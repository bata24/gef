# How to use:
# gef> source /path/to/tmux_setup.py

import os
import gdb
import atexit

def main():
    # reset panes
    try:
        gdb.execute("pi GefTmuxSetupCommand.reset_panes()", to_string=True)
    except gdb.error:
        print("GEF is not loaded")
        return

    # split
    """
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
    panes = {}
    panes["legend"] = os.popen('tmux split-window -P -F"#{pane_tty}" -h -l 30% -d "cat -"').read().strip()
    panes["regs"] = panes["legend"]
    panes["stack"] = os.popen('tmux split-window -P -F"#{pane_tty}" -v -t {bottom-right} -l 66% -d "cat -"').read().strip()
    panes["mem_access"] = panes["stack"]

    panes["code"] = os.popen('tmux split-window -P -F"#{pane_tty}" -h -l 50% -d "cat -"').read().strip()
    panes["args"] = panes["code"]
    panes["source"] = panes["code"]
    panes["trace"] = os.popen('tmux split-window -P -F"#{pane_tty}" -v -t {right-of} -l 33% -d "cat -"').read().strip()
    panes["threads"] = panes["trace"]
    panes["mem_watch"] = panes["trace"]
    panes["extra"] = panes["trace"]

    # set config
    for section, pane_tty in panes.items():
        if pane_tty:
            gdb.execute(f"gef config context_{section}.redirect {pane_tty}", to_string=True)

    # set more config
    gdb.execute(f"gef config context_code.nb_lines 16", to_string=True)
    gdb.execute(f"gef config context_code.nb_lines_prev 8", to_string=True)
    gdb.execute(f"gef config context_stack.nb_lines 16", to_string=True)

    # add atexit
    gdb.execute("pi atexit.register(GefTmuxSetupCommand.reset_panes)", to_string=True)

    # clear cache
    gdb.execute("gef reset-cache", to_string=True)

    return

if __name__ == "__main__":
    main()
