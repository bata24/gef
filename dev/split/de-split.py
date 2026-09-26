#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import ast


def module_path_to_file_path(output_dir, module_path):
    return os.path.join(output_dir, *module_path.split(".")) + ".py"


def get_comment_start(lines, start_lineno):
    start = start_lineno
    idx = start_lineno - 2
    while idx >= 0:
        if not lines[idx].lstrip().startswith("#"):
            break
        start = idx + 1
        idx -= 1
    return start


def read_function(file_path, function_name):
    with open(file_path, "r", encoding="utf-8") as f:
        src = f.read()

    tree = ast.parse(src, filename=file_path)
    lines = src.splitlines()

    for node in tree.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) or node.name != function_name:
            continue

        if node.decorator_list:
            start = min(decorator.lineno for decorator in node.decorator_list)
        else:
            start = node.lineno
        start = get_comment_start(lines, start) - 1
        return lines[start:node.end_lineno]

    raise ValueError(f"function not found in {file_path}: {function_name}")


def reconstruct():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "output")
    splitted_path = os.path.join(output_dir, "gef-splitted.py")
    output_path = os.path.join(base_dir, "gef-reconstructed.py")

    if not os.path.exists(splitted_path):
        print(f"Error: {splitted_path} not found.")
        sys.exit(1)

    with open(splitted_path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    out_lines = []

    import_re = re.compile(
        r"^(\s*)(#\s*)?from\s+(lib[a-zA-Z0-9_.]+)\s+import\s+"
        r"([a-zA-Z0-9_]+)(?:\s+as\s+([a-zA-Z0-9_]+))?"
    )
    blank_lines_re = re.compile(r"# de-split-blank-lines: ([0-9]+)\s*$")
    sys_path_re = re.compile(r"^sys\.path\.insert\(0,\s*[\"'].*?output.*?[\"']\)$")

    in_hash = False

    i = 0
    while i < len(lines):
        line = lines[i]

        if sys_path_re.match(line):
            i += 1
            if i < len(lines) and lines[i] == "":
                # Optional empty line skip if any
                pass
            continue

        m = import_re.match(line)
        if m:
            indent = m.group(1)
            commented = m.group(2) is not None
            module_path = m.group(3)
            imported_name = m.group(4)
            file_path = module_path_to_file_path(output_dir, module_path)

            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    file_content = f.read()

                if commented:
                    in_hash = False
                    out_lines.extend(file_content.splitlines())
                elif module_path.startswith("lib.hash."):
                    if not in_hash:
                        out_lines.append("class Hash:")
                        in_hash = True

                    file_lines = file_content.splitlines()
                    if file_lines and file_lines[0].strip() == "class Hash:":
                        file_lines = file_lines[1:]

                    out_lines.extend(file_lines)
                elif module_path.startswith("lib.function."):
                    in_hash = False
                    out_lines.extend(read_function(file_path, imported_name))
                else:
                    in_hash = False
                    out_lines.extend(file_content.splitlines())

                if not commented and not indent and i + 1 < len(lines):
                    next_m = import_re.match(lines[i+1])
                    if next_m:
                        if in_hash and next_m.group(3).startswith("lib.hash."):
                            blank_count = 1
                        else:
                            blank_match = blank_lines_re.search(line)
                            blank_count = int(blank_match.group(1)) if blank_match else 2
                        out_lines.extend([""] * blank_count)

                i += 1
                continue

        in_hash = False
        out_lines.append(line)
        i += 1

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines) + "\n")

    print(f"[+] Reconstructed GEF saved to {output_path}")

if __name__ == "__main__":
    reconstruct()
