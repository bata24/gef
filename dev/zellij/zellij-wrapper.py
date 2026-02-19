#!/usr/bin/env python3
# GEF Zellij Wrapper
#
# This wrapper launches Zellij with a GEF-compatible layout and starts GDB
# in the command pane. When GDB exits, the Zellij session is closed.
#
# Usage:
#   ./zellij-wrapper.py [gdb_args...]
#
# Examples:
#   ./zellij-wrapper.py             # Just start gdb
#   ./zellij-wrapper.py ./a.out     # gdb ./a.out
#   ./zellij-wrapper.py -q ./a.out  # gdb -q ./a.out
#
# NOTE: This script should be run OUTSIDE of Zellij.
#       It will create a new Zellij session with the correct layout.

import os
import sys
import glob
import subprocess

def generate_layout_kdl(gdb_args, script_path):
    """Generate a KDL layout file for GEF panes.

    Layout:
    +--------+--------+--------+
    |        | code   | legend |
    |        | args   | regs   |
    |        | source +--------+
    |        |        | stack  |
    |        +--------+ mem_acc|
    |        | others |        |
    | cmd    |        |        |
    +--------+--------+--------+
    """
    # Build the GDB command with auto-source of the setup script
    # The setup script (zellij-init.py) will be sourced in GDB to configure redirects
    init_script = os.path.join(os.path.dirname(script_path), "zellij-init.py")

    # Build args string for GDB command pane
    quoted_args = " ".join(f'"{a}"' for a in gdb_args)

    layout = """
layout {
    pane split_direction="vertical" {
        pane size="33%" focus=true {
            name "command"
            command "gdb"
            args "-ex" "source INIT_SCRIPT" GDB_ARGS
            close_on_exit true
        }
        pane size="33%" split_direction="horizontal" {
            pane size="67%" {
                name "code/args/source"
                command "bash"
                args "-c" "tty > /tmp/gef/zellij-code_args_source.tty; exec cat"
                close_on_exit true
            }
            pane size="33%" {
                name "trace/thread/mem-watch/extra"
                command "bash"
                args "-c" "tty > /tmp/gef/zellij-trace_threads_memwatch_extra.tty; exec cat"
                close_on_exit true
            }
        }
        pane size="34%" split_direction="horizontal" {
            pane size="33%" {
                name "legend/regs"
                command "bash"
                args "-c" "tty > /tmp/gef/zellij-legend_regs.tty; exec cat"
                close_on_exit true
            }
            pane size="67%" {
                name "stack/mem-access"
                command "bash"
                args "-c" "tty > /tmp/gef/zellij-stack_memaccess.tty; exec cat"
                close_on_exit true
            }
        }
    }
}
""".replace("INIT_SCRIPT", init_script).replace("GDB_ARGS", quoted_args)
    return layout


def cleanup_tty_files():
    """Remove any leftover TTY files from a previous session."""
    for f in glob.glob("/tmp/gef/zellij-*.tty"):
        try:
            os.remove(f)
        except OSError:
            pass


def main():
    # Clean up leftover TTY files
    cleanup_tty_files()

    # Generate layout
    layout_content = generate_layout_kdl(sys.argv[1:], os.path.abspath(__file__))

    # Write layout to temporary file
    layout_file = "/tmp/gef/zellij-wrapper-layout.kdl"
    with open(layout_file, "w") as f:
        f.write(layout_content)
    print(f"[zellij-wrapper] Layout written to {layout_file}")

    try:
        # Launch zellij with the layout
        print("[zellij-wrapper] Starting Zellij with GDB...")
        subprocess.run(["zellij", "--layout", layout_file], check=False)
    except KeyboardInterrupt:
        pass
    finally:
        # Clean up
        cleanup_tty_files()
        try:
            os.remove(layout_file)
        except OSError:
            pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
