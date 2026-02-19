# GEF Zellij Initializer
#
# This script configures GEF to redirect its context output to the Zellij panes.
# Place it in the same directory as `zellij-wrapper.py`.
# This script is automatically called from `zellij-wrapper.py`.
# Change `PANE_SECTIONS` to match the layout description in `zellij-wrapper.py`.

import os
import glob
import time
import signal
import subprocess

import gdb
import atexit


PANE_SECTIONS = {
    # pane_name: [gef_context_sections]
    "code_args_source": ["code", "args", "source"],
    "trace_threads_memwatch_extra": ["trace", "threads", "mem_watch", "extra"],
    "legend_regs": ["legend", "regs"],
    "stack_memaccess": ["stack", "mem_access"],
}

TTY_FILE_PREFIX = "/tmp/gef/zellij-"
TTY_FILE_SUFFIX = ".tty"

# Timeout for waiting TTY files to appear (seconds)
TTY_WAIT_TIMEOUT = 10
TTY_WAIT_INTERVAL = 0.2


def wait_for_tty_files():
    """Wait for all pane TTY files to be written and return a dict of {pane_name: tty_path}."""
    expected_panes = set(PANE_SECTIONS.keys())
    result = {}
    deadline = time.time() + TTY_WAIT_TIMEOUT

    while time.time() < deadline:
        for pane_name in list(expected_panes):
            tty_file = f"{TTY_FILE_PREFIX}{pane_name}{TTY_FILE_SUFFIX}"
            if os.path.exists(tty_file):
                try:
                    with open(tty_file, "r") as f:
                        tty_path = f.read().strip()
                    if tty_path:
                        result[pane_name] = tty_path
                        expected_panes.discard(pane_name)
                except (IOError, OSError):
                    pass

        if not expected_panes:
            return result

        time.sleep(TTY_WAIT_INTERVAL)

    if expected_panes:
        print(f"[zellij_init] Warning: Timed out waiting for TTY files: {expected_panes}")
    return result


def get_redirect_configs():
    """Return a list of GEF redirect config keys."""
    return [
        "context.redirect",
        "context_args.redirect",
        "context_code.redirect",
        "context_extra.redirect",
        "context_legend.redirect",
        "context_mem_access.redirect",
        "context_mem_watch.redirect",
        "context_regs.redirect",
        "context_source.redirect",
        "context_stack.redirect",
        "context_threads.redirect",
        "context_trace.redirect",
    ]


def configure_gef_redirects(tty_map):
    """Set GEF context section redirects based on the TTY map."""
    for pane_name, sections in PANE_SECTIONS.items():
        tty_path = tty_map.get(pane_name)
        if not tty_path:
            continue
        for section in sections:
            try:
                gdb.execute(
                    f"gef config context_{section}.redirect {tty_path}", to_string=True
                )
            except gdb.error as e:
                print(
                    f"[zellij_init] Warning: Failed to set redirect for {section}: {e}"
                )

    # Additional GEF settings
    try:
        gdb.execute("gef config context_code.nb_lines 16", to_string=True)
        gdb.execute("gef config context_code.nb_lines_prev 8", to_string=True)
        gdb.execute("gef config context_stack.nb_lines 16", to_string=True)
    except gdb.error:
        pass


def reset_gef_redirects():
    """Clear all GEF context redirect settings."""
    for config in get_redirect_configs():
        try:
            gdb.execute('gef config {:s} ""'.format(config), to_string=True)
        except gdb.error:
            pass


cleanup_state = {
    "pane_pids": [],
    "registered": False,
}


def find_cat_pids_for_ttys(tty_map):
    """Find PIDs of 'cat' processes running on the given TTYs."""
    pids = []
    for pane_name, tty_path in tty_map.items():
        try:
            result = subprocess.run(
                ["ps", "-t", tty_path.replace("/dev/", ""), "-o", "pid,comm", "--no-headers"],
                capture_output=True,
                text=True,
                timeout=3,
            )
            for line in result.stdout.strip().splitlines():
                parts = line.strip().split()
                if len(parts) >= 2 and parts[1] == "cat":
                    pids.append(int(parts[0]))
        except Exception:
            pass
    return pids


def reset_panes():
    """Reset GEF settings and kill display pane processes. Called on GDB exit."""
    reset_gef_redirects()

    for pid in cleanup_state.get("pane_pids", []):
        try:
            os.kill(pid, signal.SIGTERM)
        except (ProcessLookupError, PermissionError, OSError):
            pass

    # Clean up TTY files
    for f in glob.glob(f"{TTY_FILE_PREFIX}*{TTY_FILE_SUFFIX}"):
        try:
            os.remove(f)
        except OSError:
            pass

    try:
        atexit.unregister(reset_panes)
    except Exception:
        pass

    cleanup_state["registered"] = False


def main():
    # Check if we're in a Zellij session
    if not os.environ.get("ZELLIJ"):
        print("[zellij_init] Error: Not in a Zellij session.")
        return

    # Reset any previous pane settings from GEF tmux-setup
    try:
        gdb.execute("pi GefTmuxSetupCommand.reset_panes()", to_string=True)
    except gdb.error:
        pass

    print("[zellij_init] Waiting for display panes to initialize...")
    tty_map = wait_for_tty_files()

    if not tty_map:
        print("[zellij_init] Error: No pane TTYs discovered. Setup failed.")
        return

    # Find cat PIDs for cleanup
    cleanup_state["pane_pids"] = find_cat_pids_for_ttys(tty_map)

    # Configure GEF redirects
    configure_gef_redirects(tty_map)

    # Register cleanup on exit
    atexit.register(reset_panes)
    cleanup_state["registered"] = True

    # Clear GEF cache
    try:
        gdb.execute("gef reset-cache", to_string=True)
    except gdb.error:
        pass

    # Report success
    print("[zellij_init] Zellij panes configured successfully.")
    for pane_name, tty_path in sorted(tty_map.items()):
        sections = ", ".join(PANE_SECTIONS[pane_name])
        print(f"  {pane_name}: {tty_path} -> [{sections}]")


if __name__ == "__main__":
    main()
