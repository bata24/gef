#!/usr/bin/python3
import sys
import os
import subprocess
import requests
import json
import functools
import bisect


@functools.lru_cache
def get_chrome_info():
    url = "https://chromiumdash.appspot.com/fetch_releases?num=1"
    r = requests.get(url)
    j = json.loads(r.text)
    return j


@functools.lru_cache
def get_channel_info(channel):
    j = get_chrome_info()
    for entry in j:
        if entry["channel"].lower() == channel and entry["platform"] == "Linux":
            return entry
    raise


@functools.lru_cache
def get_valid_pos(pos):
    urlbase = "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64"
    while pos > 0:
        print(f"[!] checking {pos}...")
        url = urlbase + f"%2F{pos}%2FREVISIONS?&alt=media"
        r = requests.get(url)
        if "chromium_revision" in r.text:
            return pos
        pos -= 1
    return pos


def download_binary(channel):
    print("#"*50)
    print(f"[*] channel: {channel}")

    # preparing
    e = get_channel_info(channel)
    current_version = e["version"]
    print(f"[*] current_version: {current_version}")
    pos = e["chromium_main_branch_position"]
    print(f"[*] position: {pos}")
    pos = get_valid_pos(pos)
    print(f"[*] position where snapshot exists: {pos}")

    # check exists
    dirname = f"./chrome_{channel}"
    os.makedirs(dirname, exist_ok=True)
    if os.path.exists(f"{dirname}/chrome-linux-{pos}.zip"):
        print("  Already exists, download is skipped")
        return

    # download
    # https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=Linux_x64/
    urlbase = "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64"
    url = urlbase + f"%2F{pos}%2Fchrome-linux.zip?&alt=media"
    cmd = f"wget -O {dirname}/chrome-linux-{pos}.zip '{url}'"
    print("  Execute: {:s}".format(cmd))
    subprocess.getoutput(cmd)
    return


def print_git_url(channel):
    e = get_channel_info(channel)
    current_version = e["version"]
    pos = get_valid_pos(e["chromium_main_branch_position"])
    url_base = "https://source.chromium.org/chromium/chromium/src/+/main:base"
    dir_base = "allocator/partition_allocator/src/partition_alloc"
    commit = e["hashes"]["chromium"]

    print("[*] commit hash: {:s}".format(commit))
    print("[*] struct base::PartitionRoot")
    print("    {:s}/{:s}/partition_root.h;drc={:s}".format(url_base, dir_base, commit))
    print("[*] struct base::internal::PartitionBucket:")
    print("    {:s}/{:s}/partition_bucket.h;drc={:s}".format(url_base, dir_base, commit))
    print("[*] struct PartitionSuperPageExtentEntry:")
    print("    {:s}/{:s}/partition_superpage_extent_entry.h;drc={:s}".format(url_base, dir_base, commit))
    print("[*] struct PartitionDirectMapExtent:")
    print("    {:s}/{:s}/partition_direct_map_extent.h;drc={:s}".format(url_base, dir_base, commit))
    print("[*] struct SlotSpanMetadata:")
    print("    {:s}/{:s}/partition_page.h;drc={:s}".format(url_base, dir_base, commit))

    print("[*] v{:s}.x / {:d} / {:s}".format(current_version.split(".")[0], pos, commit))
    print()
    return


def memo():
    print("#"*50)
    print("[*] memo")
    print("  [preparation]")
    print("    disable apparmor. I added `apparmor=0` to `GRUB_CMDLINE_LINUX` in `/etc/default/grub`, then `update-grub && reboot`")
    print("  [term1]")
    print("    cd www && python3 -m http.server 8080")
    print("  [term2]")
    print("    cd chrome_stable/chrome-linux/")
    print("    rm -rf /tmp/u && sudo -u NON_ROOT_USER_NAME ./chrome --headless=new --disable-gpu "
          "--remote-debugging-port=1338 --user-data-dir=/tmp/u --enable-logging=stderr http://0:8080/inf-loop.html")
    print("  [term3 (for renderer process)]")
    print("""    gdb -q -p $(ps -ef | grep -- "--[t]ype=renderer" | awk '{pid=$2; for(i=1;i<=NF;i++) if($i ~ /--renderer-client-id=/) {split($i,a,"="); print a[2], pid}}' | sort -n | head -n 1 | awk '{print $2}')""")
    print("  [term3 (for browser process)]")
    print("""    gdb -q -p $(ps -ef | grep "\\./[c]hrome" | grep -v type | grep -v sudo | awk '{print $2}')""")
    return


if __name__ == '__main__':
    if len(sys.argv) == 1:
        channels = ["stable", "beta", "dev"]
    elif sys.argv[1] in ["-h", "--help"]:
        print("[*] usage")
        print("  python3 {:s}             # download all channels (stable, beta, dev)".format(sys.argv[0]))
        print("  python3 {:s} stable beta # download specific channel(s)".format(sys.argv[0]))
        print()
        channels = []
    else:
        channels = sys.argv[1:]

    if channels:
        for chan in channels:
            if chan in ["stable", "beta", "dev"]:
                download_binary(chan)
                print_git_url(chan)
            else:
                print("channel is stable, beta, or dev")
                exit()

    memo()
