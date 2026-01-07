import argparse
import os
import subprocess
import re
import tarfile
import difflib

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

Entries = {
    "address_space_operations": ["include/linux/fs.h"],
    "ata_port_operations": ["include/linux/libata.h"],
    "btf_kind_operations": ["kernel/bpf/btf.c"],
    "block_device_operations": ["include/linux/blkdev.h"],
    "clk_ops": ["include/linux/clk-provider.h"],
    "configfs_item_operations": ["include/linux/configfs.h"],
    "configfs_group_operations": ["include/linux/configfs.h"],
    "damon_operations": ["include/linux/damon.h"],
    "dentry_operations": ["include/linux/dcache.h"],
    "dev_pm_ops": ["include/linux/pm.h"],
    "dma_buf_ops": ["include/linux/dma-buf.h"],
    "export_operations": ["include/linux/exportfs.h"],
    "file_operations": ["include/linux/fs.h"],
    "fs_context_operations": ["include/linux/fs_context.h"],
    "inode_operations": ["include/linux/fs.h"],
    "kobj_ns_type_operations": ["include/linux/kobject_ns.h"],
    "media_entity_operations": ["include/media/media-entity.h"],
    "movable_operations": ["include/linux/migrate.h"],
    "net_device_ops": ["include/linux/netdevice.h"],
    "page_ext_operations": ["include/linux/page_ext.h"],
    "parport_operations": ["include/linux/parport.h"],
    "pernet_operations": ["include/net/net_namespace.h"],
    "pipe_buf_operations": ["include/linux/pipe_fs_i.h"],
    "proc_ns_operations": ["include/linux/proc_ns.h"],
    "proc_ops": ["include/linux/proc_fs.h"],
    "regulator_ops": ["include/linux/regulator/driver.h"],
    "seq_operations": ["include/linux/seq_file.h"],
    "smp_operations": ["arch/arm/include/asm/smp.h"],
    "super_operations": ["include/linux/fs.h", "include/linux/fs/super_types.h"],
    "tty_ldisc_ops": ["include/linux/tty_ldisc.h"],
    "tty_operations": ["include/linux/tty_driver.h"],
    "tty_port_operations": ["include/linux/tty_port.h"],
    "ucsi_operations": ["drivers/usb/typec/ucsi/ucsi.h"],
    "vm_operations_struct": ["include/linux/mm.h"],
}

def doit(args, version):
    if not os.path.exists(version.filename):
        r = os.system("wget {:s}".format(version.url))
        if r != 0:
            print("Failed to downloard")
            raise

    ops = {}
    for struct_name, filenames in Entries.items():
        found = False
        for filename in filenames:
            filepath = os.path.join(version.dirname, filename)

            if not os.path.exists(filepath):
                print("[+] Extracting... {:s}".format(filepath))
                r = os.system("tar xf {:s} '{:s}'".format(version.filename, filepath))
                if r != 0:
                    print("Failed to extract")
                    continue

            content = open(filepath).read()

            struct_name_ = "struct {:s}".format(struct_name)
            struct_lines = []
            inner = False
            for line in content.splitlines():
                if not inner:
                    if line.startswith(struct_name_) and not line.endswith(";"):
                        inner = True
                        struct_lines.append(line)
                    continue
                else:
                    struct_lines.append(line)
                    if line.startswith("}"):
                        ops[struct_name] = [filepath, struct_lines]
                        found = True
                        break
                    continue
            if found:
                break
        else:
            ops[struct_name] = [filepath, ["Not found"]]
    return ops

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("version", metavar="VERSION", type=KernelVersion, help="target version")
    parser.add_argument("version2", metavar="VERSION2", nargs="?", type=KernelVersion, help="target version for diff")
    args = parser.parse_args()

    if not args.version2:
        ops = doit(args, args.version)
        assert len(ops) == len(Entries)

        for struct_name, [filepath, lines] in ops.items():
            print("\x1b[1;37m{:s}:{:s}\x1b[00m".format(filepath, struct_name))
            for line in lines:
                print(line)
    else:
        ops1 = doit(args, args.version)
        ops2 = doit(args, args.version2)
        assert len(ops1) == len(ops2) == len(Entries)

        for struct_name in Entries.keys():
            print("\x1b[1;37m{:s}\x1b[00m".format(struct_name))
            path1, content1 = ops1[struct_name]
            path2, content2 = ops2[struct_name]
            for line in difflib.unified_diff(content1, content2, fromfile=path1, tofile=path2):
                if line[0] == "-":
                    print("\x1b[1;31m{:s}\x1b[00m".format(line)) # Red
                elif line[0] == "+":
                    print("\x1b[1;32m{:s}\x1b[00m".format(line)) # Green
                else:
                    print(line)
    return

if __name__ == "__main__":
    main()
