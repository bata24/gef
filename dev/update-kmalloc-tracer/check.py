import argparse
import os
import subprocess
import re


class KernelVersion:
    def __init__(self, version_string, download_dir="../download", extract_dir="."):
        self.version_string = version_string
        self.download_dir = download_dir
        self.extract_dir = extract_dir
        try:
            major, minor, patch, rc = self.to_version_tuple(version_string)
        except Exception as err:
            raise argparse.ArgumentTypeError from err
        self.major = major
        self.minor = minor
        self.patch = patch
        self.rc = rc
        self.version_tuple = (major, minor, patch, rc)
        return

    def to_version_tuple(self, v):
        r = re.fullmatch(r"(\d+)\.(\d+)-rc(\d+)", v)
        if r:
            return int(r.group(1)), int(r.group(2)), 0, int(r.group(3))

        r = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", v)
        if r:
            return int(r.group(1)), int(r.group(2)), int(r.group(3)), 0

        r = re.fullmatch(r"(\d+)\.(\d+)", v)
        if r:
            return int(r.group(1)), int(r.group(2)), 0, 0
        raise ValueError("Invalid kernel version: {:s}".format(v))

    def __str__(self):
        if self.rc > 0:
            return "{:d}.{:d}-rc{:d}".format(self.major, self.minor, self.rc)
        elif self.patch == 0:
            return "{:d}.{:d}".format(self.major, self.minor)
        else:
            return "{:d}.{:d}.{:d}".format(self.major, self.minor, self.patch)

    @property
    def dirname(self):
        return "linux-{:s}".format(str(self))

    @property
    def filename(self):
        if self.rc > 0:
            return "{:s}.tar.gz".format(self.dirname)
        return "{:s}.tar.xz".format(self.dirname)

    @property
    def url(self):
        if self.rc > 0:
            return "https://git.kernel.org/torvalds/t/{:s}".format(self.filename)
        return "https://cdn.kernel.org/pub/linux/kernel/v{:d}.x/{:s}".format(self.major, self.filename)

    def tarball_path(self):
        return os.path.join(self.download_dir, self.filename)

    def member_path(self, filename):
        return os.path.join(self.dirname, filename)

    def extracted_path(self, filename):
        return os.path.join(self.extract_dir, self.member_path(filename))


def check_black_list(line):
    black_list = [
        "kmalloc_caches", # variable
        "random_kmalloc_seed", # variable
        "kmalloc_dma_caches", # variable
        "kfree_const", # always calls kfree
        "kfree_sensitive", # always calls kfree
        "mempool_kfree", # always calls kfree
        "mempool_kmalloc", # always calls kmalloc
        "kmem_cache_alloc_bulk_noprof", # does not return ptr
        "kmem_cache_alloc_bulk", # does not return ptr
        "kmalloc_size_roundup", # does not return ptr
        "__kasan_kmalloc", # does not get ptr
        "kasan_kmalloc", # does not get ptr
    ]
    for f in black_list:
        f = "EXPORT_SYMBOL({:s})".format(f)
        if f in line:
            return True
    return False


def doit(args, version):
    os.makedirs(version.download_dir, exist_ok=True)
    os.makedirs(version.extract_dir, exist_ok=True)

    tarball_path = version.tarball_path()
    if not os.path.exists(tarball_path):
        r = subprocess.run(["wget", version.url, "-O", tarball_path])
        if r.returncode != 0:
            if os.path.exists(tarball_path):
                os.remove(tarball_path)
            raise RuntimeError("Failed to download")

    mm_path = version.extracted_path("mm")
    if not os.path.exists(mm_path):
        print("[+] Extracting...")
        member_path = version.member_path("mm")
        r = subprocess.run(["tar", "xf", tarball_path, "-C", version.extract_dir, member_path])
        if r.returncode != 0:
            raise RuntimeError("Failed to extract")

    cwd = os.getcwd()
    try:
        os.chdir(version.extracted_path("mm"))
        ret = subprocess.getoutput("grep -r EXPORT_SYMBOL |egrep 'kmalloc|krealloc|kfree|kmem_cache_alloc'")
    finally:
        os.chdir(cwd)

    lines = []
    for line in ret.splitlines():
        if check_black_list(line):
            continue
        line = re.sub(r"\((.+?)\)", lambda x: "(" + '\x1b[1;37m' + x.group(1) + '\x1b[00m' + ")", line)
        if args.simple:
            line = line.split(":")[1]
        lines.append(line)
    return sorted(set(lines))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--download-dir", default="../download", help="download directory")
    parser.add_argument("-e", "--extract-dir", default=".", help="extract directory")
    parser.add_argument("version", metavar="VERSION", help="target version")
    parser.add_argument("version2", metavar="VERSION2", nargs="?", help="target version for diff")
    parser.add_argument("-s", "--simple", action="store_true", help="omit source filename")
    args = parser.parse_args()

    version = KernelVersion(args.version, args.download_dir, args.extract_dir)
    version2 = None
    if args.version2:
        version2 = KernelVersion(args.version2, args.download_dir, args.extract_dir)

    if not version2:
        lines = doit(args, version)
        for line in lines:
            print(line)
    else:
        lines = doit(args, version)
        lines2 = doit(args, version2)

        print("#" * 30 + version.dirname)

        for line in lines:
            if line in lines2:
                continue
            print(line)

        print("#" * 30 + version2.dirname)

        for line in lines2:
            if line in lines:
                continue
            print(line)


if __name__ == "__main__":
    main()
