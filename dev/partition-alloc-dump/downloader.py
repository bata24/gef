#!/usr/bin/python3
import argparse
import os
import subprocess
import requests
import functools
import shlex
from urllib.parse import quote


ARCHES = {
    "x64": ("Linux", "Linux_x64", "chrome-linux.zip"),
    "arm": ("Android", "Android", "chrome-android.zip"),
    "arm64": ("Android", "Android_Arm64", "chrome-android.zip"),
}
SNAPSHOTS = "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o"
DEBIAN_CHROMIUM = "https://deb.debian.org/debian/pool/main/c/chromium"
DEBIAN_BUILDS = {
    "x64": ("amd64", "156.0.8078.79-1~deb13u1"),
    "x86": ("i386", "156.0.8078.79-1~deb13u1"),
    "arm": ("armhf", "150.0.7871.181-1~deb13u1"),
    "arm64": ("arm64", "156.0.8078.79-1~deb13u1"),
}


@functools.lru_cache
def get_chrome_info():
    url = "https://chromiumdash.appspot.com/fetch_releases?num=1"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    j = r.json()
    return j


@functools.lru_cache
def get_channel_info(channel, arch):
    j = get_chrome_info()
    for entry in j:
        if entry["channel"].lower() == channel and entry["platform"] == ARCHES[arch][0]:
            return entry
    raise RuntimeError(f"No release information for {channel}/{arch}")


@functools.lru_cache
def get_valid_pos(pos, platform, archive):
    # Search nearby snapshots without falling back to an obsolete architecture build.
    for block in (pos // 10000, pos // 10000 - 1):
        params = {"prefix": f"{platform}/{block}", "delimiter": "/", "fields": "prefixes,nextPageToken"}
        candidates = []
        while True:
            r = requests.get(
                "https://storage.googleapis.com/storage/v1/b/chromium-browser-snapshots/o", params=params, timeout=30,
            )
            r.raise_for_status()
            listing = r.json()
            for prefix in listing.get("prefixes", []):
                revision = int(prefix.split("/")[1])
                if pos - 10000 <= revision <= pos:
                    candidates.append(revision)
            if "nextPageToken" not in listing:
                break
            params["pageToken"] = listing["nextPageToken"]
        for revision in sorted(candidates, reverse=True):
            print(f"[!] checking {platform}/{revision}...")
            key = quote(f"{platform}/{revision}/{archive}", safe="")
            r = requests.head(f"{SNAPSHOTS}/{key}?alt=media", timeout=30)
            if r.status_code == 200:
                return revision
            if r.status_code != 404:
                r.raise_for_status()
    raise RuntimeError(f"No recent {platform} snapshot near {pos}; this architecture may no longer be published")


def get_download_dir(channel, arch, source):
    dirname = f"./chrome_{channel}"
    if arch != "x64":
        dirname += f"_{arch}"
    if source == "debian" and arch != "x86":
        dirname += "_debian"
    return dirname


def download_file(url, destination):
    # check exists
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    if os.path.exists(destination):
        print(f"  Already exists, download is skipped: {destination}")
        return

    # download
    cmd = ["wget", "-O", destination + ".part", url]
    print("  Execute: " + shlex.join(cmd))
    subprocess.run(cmd, check=True)
    os.replace(destination + ".part", destination)
    return


def download_binary(channel, arch, source):
    print("#"*50)
    print(f"[*] channel: {channel}")
    print(f"[*] arch: {arch}")
    print(f"[*] distribution: {source}")
    dirname = get_download_dir(channel, arch, source)

    if source == "debian":
        deb_arch, version = DEBIAN_BUILDS[arch]
        print(f"[*] platform: Linux (Debian {deb_arch})")
        print(f"[*] source: {DEBIAN_CHROMIUM}/")
        print(f"[*] package_version: {version}")
        print("[*] Chromium release channels do not apply; using the pinned Debian prebuilt.")
        for package in ("chromium-headless-shell", "chromium-common"):
            filename = f"{package}_{version}_{deb_arch}.deb"
            download_file(f"{DEBIAN_CHROMIUM}/{filename}", f"{dirname}/{filename}")
        return None

    release_platform, platform, archive = ARCHES[arch]
    print(f"[*] platform: {release_platform} ({platform})")

    # preparing
    e = get_channel_info(channel, arch)
    current_version = e["version"]
    print(f"[*] current_version: {current_version}")
    pos = e["chromium_main_branch_position"]
    print(f"[*] position: {pos}")
    pos = get_valid_pos(pos, platform, archive)
    print(f"[*] position where snapshot exists: {pos}")

    filename = archive.replace(".zip", f"-{pos}.zip")
    destination = f"{dirname}/{filename}"

    # download
    # https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html
    key = quote(f"{platform}/{pos}/{archive}", safe="")
    url = f"{SNAPSHOTS}/{key}?alt=media"
    download_file(url, destination)
    return pos


def print_git_url(channel, arch, pos):
    e = get_channel_info(channel, arch)
    current_version = e["version"]
    url_base = "https://source.chromium.org/chromium/chromium/src/+/main:base"
    dir_base = "allocator/partition_allocator/src/partition_alloc"
    platform = ARCHES[arch][1]
    key = quote(f"{platform}/{pos}/REVISIONS", safe="")
    response = requests.get(f"{SNAPSHOTS}/{key}?alt=media", timeout=30)
    response.raise_for_status()
    # Release hashes describe the requested channel, not necessarily the nearby snapshot we downloaded.
    commit = response.json()["got_revision"]

    print("[*] commit hash: {:s}".format(commit))
    print("[*] struct partition_alloc::PartitionRoot")
    print("    {:s}/{:s}/partition_root.h;drc={:s}".format(url_base, dir_base, commit))
    print("[*] struct partition_alloc::internal::PartitionBucket:")
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


def memo(arch, channel, source):
    print("#"*50)
    print(f"[*] memo: {source} / {arch}")
    dirname = get_download_dir(channel, arch, source)
    if source == "debian":
        print("  [term1]")
        print("    cd www && python3 -m http.server 8080")
        print("  [term2]")
        print(f"    sudo apt install {dirname}/*.deb")
        print("    /usr/lib/chromium/chromium-headless-shell --no-sandbox --disable-gpu "
              "--remote-debugging-port=1338 http://localhost:8080/inf-loop.html")
        return
    if ARCHES[arch][0] == "Android":
        print(f"    unzip -d {dirname} {dirname}/chrome-android-*.zip")
        print(f"    adb install -r {dirname}/chrome-android/apks/ChromePublic.apk")
        return
    print("  [term1]")
    print("    cd www && python3 -m http.server 8080")
    print("  [term2]")
    print(f"    unzip -d /tmp {dirname}/chrome-linux-*.zip && cd /tmp/chrome-linux")
    print("    rm -rf /tmp/u && sudo -u NON_ROOT_USER_NAME ./chrome --headless=new --disable-gpu --no-sandbox "
          "--remote-debugging-port=1338 --user-data-dir=/tmp/u --enable-logging=stderr http://localhost:8080/inf-loop.html")
    print("  [term3 (for renderer process)]")
    print("""    gdb -q -p $(ps -ef | grep -- "--[t]ype=renderer" | awk '{pid=$2; for(i=1;i<=NF;i++) """
          """if($i ~ /--renderer-client-id=/) {split($i,a,"="); print a[2], pid}}' | sort -n | head -n 1 | awk '{print $2}')""")
    print("  [term3 (for browser process)]")
    print("""    gdb -q -p $(ps -ef | grep "\\./[c]hrome" | grep -v type | grep -v sudo | awk '{print $2}')""")
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Download official Chromium snapshots or Debian packages.")
    parser.add_argument("channels", nargs="*", metavar="CHANNEL",
                        help="stable, beta, dev (default: all; Debian-only: dev output directory)")
    parser.add_argument("-a", "--arch", choices=("x64", "x86", "arm", "arm64"), default="x64",
                        help="target architecture (default: %(default)s)")
    parser.add_argument("-s", "--source", choices=("auto", "official", "debian", "both"), default="auto",
                        help="auto: x86=Debian, others=official; official ARM builds are Android APKs")
    args = parser.parse_args()
    if args.source == "auto":
        if args.arch == "x86":
            sources = ["debian"]
        else:
            sources = ["official"]
    elif args.source == "both":
        sources = ["official", "debian"]
    else:
        sources = [args.source]
    if "official" in sources and args.arch not in ARCHES:
        parser.error("official x86 snapshots are unavailable; use --source debian")
    channels = args.channels
    if not channels:
        if sources == ["debian"]:
            channels = ["dev"]
        else:
            channels = ["stable", "beta", "dev"]
    for chan in channels:
        if chan not in ["stable", "beta", "dev"]:
            parser.error("channel must be stable, beta, or dev")
    try:
        for chan in channels:
            for source in sources:
                pos = download_binary(chan, args.arch, source)
                if pos is not None:
                    print_git_url(chan, args.arch, pos)
    except (RuntimeError, requests.RequestException, subprocess.CalledProcessError) as error:
        parser.exit(1, f"[!] {error}\n")
    for source in sources:
        memo(args.arch, channels[-1], source)
