#!/usr/bin/python3
# This file simply splits each class into a separate file for AI code review.
# Dependencies will not be resolved, so splitting GEF will not work correctly.

import os
import re
import ast
import shutil


def get_comment_start(lines, start_lineno):
    start = start_lineno
    idx = start_lineno - 2
    while idx >= 0:
        if not lines[idx].lstrip().startswith("#"):
            break
        start = idx + 1
        idx -= 1
    return start


def class_ranges_from_file(path):
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()

    tree = ast.parse(src, filename=path)
    result = {}

    tops = [n for n in tree.body if hasattr(n, "lineno")]

    for node in tops:
        if not isinstance(node, ast.ClassDef):
            continue

        if node.decorator_list:
            start = min(d.lineno for d in node.decorator_list)
        else:
            start = node.lineno

        end = node.end_lineno
        result[node.name] = (start - 1, end)

    return result


def global_ranges_from_file(path):
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()

    tree = ast.parse(src, filename=path)
    lines = src.splitlines()
    result = {}

    tops = [n for n in tree.body if hasattr(n, "lineno")]

    for node in tops:
        name = None

        if isinstance(node, ast.Assign):
            if len(node.targets) != 1:
                continue
            if not isinstance(node.targets[0], ast.Name):
                continue
            name = node.targets[0].id
        elif isinstance(node, ast.AnnAssign):
            if not isinstance(node.target, ast.Name):
                continue
            name = node.target.id
        else:
            continue

        if ("syscall_defs" not in name) and ("syscall_tbl" not in name) and ("syscall_list" not in name):
            continue

        start = get_comment_start(lines, node.lineno)
        end = node.end_lineno
        result[name] = (start - 1, end)

    return result


def top_level_function_ranges_from_file(path):
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()

    tree = ast.parse(src, filename=path)
    lines = src.splitlines()

    result = {}
    for node in tree.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue

        if node.decorator_list:
            start = min(d.lineno for d in node.decorator_list)
        else:
            start = node.lineno

        start = get_comment_start(lines, start)
        end = node.end_lineno
        result[node.name] = (start - 1, end)

    return result


def used_decorator_names_from_file(path):
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()

    tree = ast.parse(src, filename=path)
    used_decorators = set()

    def add_decorator_name(expr):
        target = expr
        if isinstance(target, ast.Call):
            target = target.func

        if isinstance(target, ast.Name):
            used_decorators.add(target.id)
            return

        if isinstance(target, ast.Attribute):
            used_decorators.add(target.attr)
            return

    for node in ast.walk(tree):
        if not isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for deco in node.decorator_list:
            add_decorator_name(deco)

    return used_decorators


def function_groups_from_file(path):
    top_level_funcs = top_level_function_ranges_from_file(path)
    used_decorators = used_decorator_names_from_file(path)

    decorator_dic = {}
    rw_dic = {}
    checker_dic = {}

    forced_decorators = {"perf", "cperf"}

    for name, rng in top_level_funcs.items():
        if name in used_decorators or name in forced_decorators:
            decorator_dic[name] = rng
            continue

        if re.match(r"^(read|write)_[A-Za-z0-9_]+$", name):
            rw_dic[name] = rng
            continue

        if re.match(r"^is_[A-Za-z0-9_]+$", name) or name in ["kgdb_has_system_registers"]:
            checker_dic[name] = rng
            continue

    return {
        "decorator": decorator_dic,
        "rw": rw_dic,
        "checker": checker_dic,
    }


def hash_groups_from_file(path):
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()

    tree = ast.parse(src, filename=path)
    lines = src.splitlines()

    hash_node = None
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == "Hash":
            hash_node = node
            break

    if hash_node is None:
        return None

    nested_classes = []
    nested_names = set()

    for node in hash_node.body:
        if not isinstance(node, ast.ClassDef):
            continue
        nested_classes.append(node)
        nested_names.add(node.name)

    ranges = {}
    base_map = {}
    order = []

    for node in nested_classes:
        if node.decorator_list:
            start = min(d.lineno for d in node.decorator_list)
        else:
            start = node.lineno
        start = get_comment_start(lines, start)
        end = node.end_lineno

        ranges[node.name] = (start - 1, end)
        order.append(node.name)

        base_name = None
        if len(node.bases) > 1:
            raise ValueError(f"multiple inheritance is not supported: Hash.{node.name}")

        if node.bases:
            base = node.bases[0]
            if isinstance(base, ast.Name) and base.id in nested_names:
                base_name = base.id
            elif (
                isinstance(base, ast.Attribute)
                and isinstance(base.value, ast.Name)
                and base.value.id == "Hash"
                and base.attr in nested_names
            ):
                base_name = base.attr

        base_map[node.name] = base_name

    def root_of(name):
        cur = name
        seen = set()
        while base_map[cur] is not None:
            if cur in seen:
                raise ValueError(f"cyclic inheritance detected under Hash: {name}")
            seen.add(cur)
            cur = base_map[cur]
        return cur

    groups = {}
    for name in order:
        root = root_of(name)
        if root not in groups:
            groups[root] = []
        groups[root].append(name)

    hash_start = min(d.lineno for d in hash_node.decorator_list) if hash_node.decorator_list else hash_node.lineno
    hash_start = get_comment_start(lines, hash_start)
    hash_end = hash_node.end_lineno

    return {
        "hash_range": (hash_start - 1, hash_end),
        "groups": groups,
        "ranges": ranges,
        "order": order,
    }


def write_hash_groups(path, save_dir, hash_info):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    hash_dir = os.path.join(save_dir, "lib", "hash")
    if not os.path.exists(hash_dir):
        os.mkdir(hash_dir)

    group_imports = []
    order_index = {name: idx for idx, name in enumerate(hash_info["order"])}

    for root_name, class_names in sorted(
        hash_info["groups"].items(),
        key=lambda item: order_index[item[0]],
    ):
        sorted_names = sorted(class_names, key=lambda name: order_index[name])
        chunks = []

        for class_name in sorted_names:
            s, e = hash_info["ranges"][class_name]
            chunks.extend(lines[s:e])
            chunks.append("")

        if chunks and chunks[-1] == "":
            chunks.pop()

        out_lines = ["class Hash:"]
        out_lines.extend(chunks)

        file_path = os.path.join(hash_dir, root_name + ".py")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(out_lines) + "\n")

        alias = f"Hash__{root_name}"
        group_imports.append(f"from lib.hash.{root_name} import Hash as {alias}")

    return group_imports


def collapse_blank_lines_between_from_imports(lines):
    result = []
    i = 0

    def is_from_import(line):
        return line.startswith("from ") and " import " in line

    while i < len(lines):
        line = lines[i]
        if is_from_import(line):
            result.append(line)
            j = i + 1
            while j < len(lines) and lines[j] == "":
                j += 1
            if j < len(lines) and is_from_import(lines[j]):
                i = j
                continue
            i += 1
            continue

        result.append(line)
        i += 1

    return result


def split_gef(path, class_dic, global_dic, function_groups, save_dir):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    hash_info = hash_groups_from_file(path)
    hash_imports = []

    new_gef = []
    pos = 0

    items = []
    for class_name, (s, e) in class_dic.items():
        items.append(("class", class_name, s, e))
    for global_name, (s, e) in global_dic.items():
        items.append(("global", global_name, s, e))
    for decorator_name, (s, e) in function_groups["decorator"].items():
        items.append(("decorator", decorator_name, s, e))
    for rw_name, (s, e) in function_groups["rw"].items():
        items.append(("rw", rw_name, s, e))
    for checker_name, (s, e) in function_groups["checker"].items():
        items.append(("checker", checker_name, s, e))

    if hash_info is not None:
        hash_s, hash_e = hash_info["hash_range"]
        items = [item for item in items if not (item[0] == "class" and item[1] == "Hash")]
        items.append(("hash", "Hash", hash_s, hash_e))
        hash_imports = write_hash_groups(path, save_dir, hash_info)

    items.sort(key=lambda x: x[2])

    for item_type, name, s, e in items:
        new_gef.extend(lines[pos:s])
        code = lines[s:e]

        if item_type == "class":
            if name.endswith("Command"):
                file_path = os.path.join(save_dir, "lib", "command", name + ".py")
                new_gef.append(f"from lib.command.{name} import {name}")
            elif (s + 1) < len(lines) and ("GEF representation of " in lines[s + 1]) and ("architecture." in lines[s + 1]):
                file_path = os.path.join(save_dir, "lib", "arch", name + ".py")
                new_gef.append(f"from lib.arch.{name} import {name}")
            else:
                file_path = os.path.join(save_dir, "lib", name + ".py")
                new_gef.append(f"from lib.{name} import {name}")

            with open(file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(code))
        elif item_type == "global":
            file_path = os.path.join(save_dir, "lib", "syscall", name + ".py")
            new_gef.append(f"from lib.syscall.{name} import {name}")

            with open(file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(code))
        elif item_type == "decorator":
            file_path = os.path.join(save_dir, "lib", "decorator", name + ".py")
            new_gef.append(f"from lib.decorator.{name} import {name}")

            with open(file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(code))
        elif item_type == "rw":
            file_path = os.path.join(save_dir, "lib", "rw", name + ".py")
            new_gef.append(f"from lib.rw.{name} import {name}")

            with open(file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(code))
        elif item_type == "checker":
            file_path = os.path.join(save_dir, "lib", "checker", name + ".py")
            new_gef.append(f"from lib.checker.{name} import {name}")

            with open(file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(code))
        elif item_type == "hash":
            new_gef.extend(hash_imports)
        else:
            raise ValueError(f"unknown item type: {item_type}")

        pos = e

    new_gef.extend(lines[pos:])

    idx = new_gef.index("import traceback") + 1
    new_gef = (
        new_gef[:idx]
        + ['sys.path.insert(0, "' + os.path.join(os.path.dirname(__file__), "save") + '")']
        + new_gef[idx:]
    )

    new_gef = collapse_blank_lines_between_from_imports(new_gef)

    file_name = os.path.join(save_dir, "gef-splitted.py")
    with open(file_name, "w", encoding="utf-8") as f:
        f.write("\n".join(new_gef))

    return


if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    save_dir = os.path.join(base_dir, "save")
    if os.path.exists(save_dir):
        shutil.rmtree(save_dir)

    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    if not os.path.exists(os.path.join(save_dir, "lib")):
        os.mkdir(os.path.join(save_dir, "lib"))
    if not os.path.exists(os.path.join(save_dir, "lib", "command")):
        os.mkdir(os.path.join(save_dir, "lib", "command"))
    if not os.path.exists(os.path.join(save_dir, "lib", "arch")):
        os.mkdir(os.path.join(save_dir, "lib", "arch"))
    if not os.path.exists(os.path.join(save_dir, "lib", "syscall")):
        os.mkdir(os.path.join(save_dir, "lib", "syscall"))
    if not os.path.exists(os.path.join(save_dir, "lib", "hash")):
        os.mkdir(os.path.join(save_dir, "lib", "hash"))
    if not os.path.exists(os.path.join(save_dir, "lib", "decorator")):
        os.mkdir(os.path.join(save_dir, "lib", "decorator"))
    if not os.path.exists(os.path.join(save_dir, "lib", "rw")):
        os.mkdir(os.path.join(save_dir, "lib", "rw"))
    if not os.path.exists(os.path.join(save_dir, "lib", "checker")):
        os.mkdir(os.path.join(save_dir, "lib", "checker"))

    gef_path = os.path.normpath(os.path.join(base_dir, "../../gef.py"))
    class_dic = class_ranges_from_file(gef_path)
    global_dic = global_ranges_from_file(gef_path)
    function_groups = function_groups_from_file(gef_path)
    split_gef(gef_path, class_dic, global_dic, function_groups, save_dir)
