import argparse
import os
import subprocess
import re

class KernelVersion:
    def __init__(self, version_string):
        self.version_string = version_string
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
        r = re.match(r"(\d+)\.(\d+)-rc(\d+)", v)
        if r:
            return int(r.group(1)), int(r.group(2)), 0, int(r.group(3))

        r = re.match(r"(\d+)\.(\d+)\.(\d+)", v)
        if r:
            return int(r.group(1)), int(r.group(2)), int(r.group(3)), 0

        r = re.match(r"(\d+)\.(\d+)", v)
        if r:
            return int(r.group(1)), int(r.group(2)), 0, 0
        raise

    def __str__(self):
        if self.rc > 0:
            return "{:d}.{:d}-rc{:d}".format(self.major, self.minor, self.rc)
        elif self.patch == 0:
            return "{:d}.{:d}".format(self.major, self.minor)
        else:
            return "{:d}.{:d}.{:d}".format(self.major, self.minor, self.patch)
        raise

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

def check_black_list(line):
    black_list = [
        "kmalloc_caches", # variable
        "random_kmalloc_seed", # variable
        "kmalloc_dma_caches", # variable
        "kfree_const", # always call kfree
        "kfree_sensitive", # always call kfree
        "mempool_kfree", # always call kfree
        "mempool_kmalloc", # always call kmalloc
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
    if not os.path.exists(version.filename):
        os.system("wget {:s}".format(version.url))

    if not os.path.exists(version.dirname):
        print("[+] Extracting...")
        os.system("tar xf {:s} '{:s}/mm/'".format(version.filename, version.dirname))

    os.chdir(os.path.join(version.dirname, "mm"))
    ret = subprocess.getoutput("grep -r EXPORT_SYMBOL |egrep 'kmalloc|krealloc|kfree|kmem_cache_alloc'")
    os.chdir("../..")

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
    parser.add_argument("version", metavar="VERSION", type=KernelVersion, help="rc edition is unsupported")
    parser.add_argument("version2", metavar="VERSION2", nargs="?", type=KernelVersion, help="rc edition is unsupported")
    parser.add_argument("-s", "--simple", action="store_true", help="omit source filename")
    args = parser.parse_args()

    if not args.version2:
        lines = doit(args, args.version)
        for line in lines:
            print(line)
    else:
        lines = doit(args, args.version)
        lines2 = doit(args, args.version2)

        print("#" * 30 + args.version.dirname)

        for line in lines:
            if line in lines2:
                continue
            print(line)

        print("#" * 30 + args.version2.dirname)

        for line in lines2:
            if line in lines:
                continue
            print(line)

if __name__ == "__main__":
    main()
