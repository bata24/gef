#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

def reconstruct():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    save_dir = os.path.join(base_dir, "save")
    splitted_path = os.path.join(save_dir, "gef-splitted.py")
    output_path = os.path.join(base_dir, "gef-reconstructed.py")

    if not os.path.exists(splitted_path):
        print(f"Error: {splitted_path} not found.")
        sys.exit(1)

    with open(splitted_path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    out_lines = []

    import_re = re.compile(r"^from\s+(lib[a-zA-Z0-9_.]+)\s+import\s+([a-zA-Z0-9_]+)(?:\s+as\s+([a-zA-Z0-9_]+))?")
    sys_path_re = re.compile(r"^sys\.path\.insert\(0,\s*[\"'].*?save.*?[\"']\)$")

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
            module_path = m.group(1)
            file_path = os.path.join(save_dir, *module_path.split(".")) + ".py"

            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    file_content = f.read()

                if module_path.startswith("lib.hash."):
                    if not in_hash:
                        out_lines.append("class Hash:")
                        in_hash = True

                    file_lines = file_content.splitlines()
                    if file_lines and file_lines[0].strip() == "class Hash:":
                        file_lines = file_lines[1:]

                    out_lines.extend(file_lines)
                else:
                    in_hash = False
                    out_lines.extend(file_content.splitlines())

                # adding blank lines to restore what `collapse_blank_lines_between_from_imports` removed
                if i + 1 < len(lines):
                    next_m = import_re.match(lines[i+1])
                    if next_m:
                        next_is_hash = next_m.group(1).startswith("lib.hash.")
                        if in_hash and next_is_hash:
                            out_lines.append("")
                        else:
                            out_lines.append("")
                            out_lines.append("")

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
