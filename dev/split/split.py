#!/usr/bin/python3
# This file simply splits each class into a separate file for AI code review.
# Dependencies will not be resolved, so splitting GEF will not work correctly.

import os
import ast
import shutil


def class_ranges_from_file(path):
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()

    tree = ast.parse(src, filename=path)
    result = {}

    # top level node (with lineno only)
    tops = [n for n in tree.body if hasattr(n, "lineno")]

    for i, node in enumerate(tops):
        if not isinstance(node, ast.ClassDef):
            continue

        # start lineno: include decorator if exists
        if node.decorator_list:
            start = min(d.lineno for d in node.decorator_list)
        else:
            start = node.lineno

        # end lineno:
        end = node.end_lineno

        result[node.name] = (start - 1, end)  # 1-index -> 0-index

    return result


def global_ranges_from_file(path):
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()

    tree = ast.parse(src, filename=path)
    lines = src.splitlines()
    result = {}

    def get_comment_start(start_lineno):
        start = start_lineno
        idx = start_lineno - 2
        while idx >= 0:
            if not lines[idx].lstrip().startswith("#"):
                break
            start = idx + 1
            idx -= 1
        return start

    # top level node (with lineno only)
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

        start = get_comment_start(node.lineno)
        end = node.end_lineno
        result[name] = (start - 1, end)  # 1-index -> 0-index

    return result


def split_gef(path, class_dic, global_dic, save_dir):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    new_gef = []
    pos = 0

    items = []
    for class_name, (s, e) in class_dic.items():
        items.append(("class", class_name, s, e))
    for global_name, (s, e) in global_dic.items():
        items.append(("global", global_name, s, e))
    items.sort(key=lambda x: x[2])

    for item_type, name, s, e in items:
        new_gef.extend(lines[pos:s])
        code = lines[s:e]

        if item_type == "class":
            if name.endswith("Command"):
                file_path = os.path.join(save_dir, "lib", "command", name + ".py")
                new_gef.append(f"from lib.command.{name} import {name}")
            elif ("GEF representation of " in lines[s + 1]) and ("architecture." in lines[s + 1]):
                file_path = os.path.join(save_dir, "lib", "arch", name + ".py")
                new_gef.append(f"from lib.arch.{name} import {name}")
            else:
                file_path = os.path.join(save_dir, "lib", name + ".py")
                new_gef.append(f"from lib.{name} import {name}")
        else:
            file_path = os.path.join(save_dir, "lib", "syscall", name + ".py")
            new_gef.append(f"from lib.syscall.{name} import {name}")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(code))
        pos = e

    new_gef.extend(lines[pos:])

    idx = new_gef.index("import traceback") + 1
    new_gef = (
        new_gef[:idx]
        + ['sys.path.insert(0, "' + os.path.join(os.path.dirname(__file__), "save") + '")']
        + new_gef[idx:]
    )

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

    gef_path = os.path.normpath(os.path.join(base_dir, "../../gef.py"))
    class_dic = class_ranges_from_file(gef_path)
    global_dic = global_ranges_from_file(gef_path)
    split_gef(gef_path, class_dic, global_dic, save_dir)
