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
    lines = src.splitlines()
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

        result[node.name] = (start - 1, end) # 1-index -> 0-index

    return result

def split_gef(path, dic, save_dir):
    lines = open(path).read().splitlines()

    new_gef = []
    pos = 0
    for class_name, (s, e) in dic.items():
        new_gef.extend(lines[pos:s])
        class_code = lines[s:e]

        if class_name.endswith("Command"):
            file_path = os.path.join(save_dir, "lib", "command", class_name + ".py")
            new_gef.append(f"from lib.command.{class_name} import {class_name}")
        elif ("GEF representation of " in lines[s + 1]) and ("architecture." in lines[s + 1]):
            file_path = os.path.join(save_dir, "lib", "arch", class_name + ".py")
            new_gef.append(f"from lib.arch.{class_name} import {class_name}")
        else:
            file_path = os.path.join(save_dir, "lib", class_name + ".py")
            new_gef.append(f"from lib.{class_name} import {class_name}")

        open(file_path, "w").write("\n".join(class_code))
        pos = e

    new_gef.extend(lines[pos:])

    idx = new_gef.index("import traceback") + 1
    new_gef = new_gef[:idx] + ['sys.path.insert(0, "' + os.path.join(os.path.dirname(__file__), "save") + '")'] + new_gef[idx:]

    file_name = os.path.join(save_dir, "gef-splitted.py")
    open(file_name, "w").write("\n".join(new_gef))
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

    gef_path = os.path.normpath(os.path.join(base_dir, "../../gef.py"))
    dic = class_ranges_from_file(gef_path)
    split_gef(gef_path, dic, save_dir)
