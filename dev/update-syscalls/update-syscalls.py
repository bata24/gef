import argparse
import difflib
import hashlib
import os
import posixpath
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile


class KernelVersion:
    def __init__(self, version_string, download_dir="../download", extract_dir="."):
        self.version_string = version_string
        self.download_dir = download_dir
        self.extract_dir = extract_dir
        try:
            major, minor, patch, rc = self.to_version_tuple(version_string)
        except Exception as err:
            raise argparse.ArgumentTypeError(str(err)) from err
        self.major = major
        self.minor = minor
        self.patch = patch
        self.rc = rc
        self.version_tuple = (major, minor, patch, rc)
        return

    def to_version_tuple(self, value):
        result = re.fullmatch(r"(\d+)\.(\d+)-rc(\d+)", value)
        if result:
            return int(result.group(1)), int(result.group(2)), 0, int(result.group(3))

        result = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", value)
        if result:
            return int(result.group(1)), int(result.group(2)), int(result.group(3)), 0

        result = re.fullmatch(r"(\d+)\.(\d+)", value)
        if result:
            return int(result.group(1)), int(result.group(2)), 0, 0
        raise ValueError("Invalid kernel version: {:s}".format(value))

    def version_name(self):
        if self.rc > 0:
            return "{:d}.{:d}-rc{:d}".format(self.major, self.minor, self.rc)
        elif self.patch == 0:
            return "{:d}.{:d}".format(self.major, self.minor)
        else:
            return "{:d}.{:d}.{:d}".format(self.major, self.minor, self.patch)

    @property
    def dirname(self):
        return "linux-{:s}".format(self.version_name())

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

    def source_dir(self):
        return os.path.join(self.extract_dir, self.dirname)


class ScriptContext:
    def __init__(self, args, work_dir):
        self.args = args
        self.kernel = args.version
        self.gef_dir = args.gef_dir
        self.gef_path = os.path.join(args.gef_dir, "gef.py")
        self.gef_tmp_path = args.output
        self.in_place = args.in_place
        self.work_dir = work_dir
        self.tmp_a = os.path.join(work_dir, "a")
        self.tmp_b = os.path.join(work_dir, "b")
        self.clang_format = which("clang-format")

        if self.gef_tmp_path is None:
            if self.in_place:
                self.gef_tmp_path = os.path.join(work_dir, "gef.py.tmp")
            else:
                self.gef_tmp_path = self.gef_path + ".tmp"
        return


################################################################################
# init and arguments check


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--download-dir", default="../download", help="download directory")
    parser.add_argument("-e", "--extract-dir", default=".", help="extract directory")
    parser.add_argument("-o", "--output", help="output path for patched gef.py")
    parser.add_argument("--in-place", action="store_true", help="update gef.py directly")
    parser.add_argument("gef_dir", metavar="GEF_DIR", help="GEF repository directory")
    parser.add_argument("version", metavar="VERSION", help="target kernel version")
    args = parser.parse_args()

    if args.in_place and args.output:
        parser.error("--in-place and --output cannot be used together")

    try:
        args.version = KernelVersion(args.version, args.download_dir, args.extract_dir)
    except argparse.ArgumentTypeError as err:
        parser.error(str(err))

    return args


def init_context(args, work_dir):
    context = ScriptContext(args, work_dir)

    if not os.path.exists(context.gef_dir):
        raise RuntimeError("Not found {:s}".format(context.gef_dir))

    if not os.path.exists(context.gef_path):
        raise RuntimeError("Not found {:s}".format(context.gef_path))

    if os.path.abspath(context.gef_tmp_path) == os.path.abspath(context.gef_path):
        raise RuntimeError("Output path must differ from gef.py. Use --in-place instead.")

    output_dir = os.path.dirname(os.path.abspath(context.gef_tmp_path))
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    if os.path.exists(context.gef_tmp_path):
        os.unlink(context.gef_tmp_path)

    shutil.copyfile(context.gef_path, context.gef_tmp_path)
    return context


def print_patch_result(context):
    print(titlify("patch result"))
    original_hash = hashlib.sha1(open(context.gef_path, "rb").read()).hexdigest()
    patched_hash = hashlib.sha1(open(context.gef_tmp_path, "rb").read()).hexdigest()
    if original_hash == patched_hash:
        print("[+] No diff")
        os.unlink(context.gef_tmp_path)
        return

    if context.in_place:
        shutil.copyfile(context.gef_tmp_path, context.gef_path)
        os.unlink(context.gef_tmp_path)
        print("[+] patched gef.py is saved to {:s}".format(context.gef_path))
        return

    print("[+] patched gef.py is saved to {:s}".format(context.gef_tmp_path))
    return


################################################################################
# utility


def get_terminal_size():
    try:
        size = shutil.get_terminal_size((100, 600))
        return size.lines, size.columns
    except OSError:
        return 600, 100


def titlify(text):
    cols = get_terminal_size()[1]
    cs = "\033[36m" # cyan
    ce = "\033[0m" # normal

    msg = []
    if text:
        nb = max((cols - len(text) - 2) // 2, 0)
        msg.append(cs + "{} ".format("-" * nb) + ce)
        msg.append(cs + text + ce)
        msg.append(cs + " {}".format("-" * nb) + ce)
    else:
        msg.append(cs + "{}".format("-" * cols) + ce)
    return "".join(msg)


def which(command):
    path = shutil.which(command)
    if not path:
        raise RuntimeError("Not found {:s}".format(command))
    return path


def read_text(path):
    return open(path, "rb").read().decode("ascii")


def write_text(path, text):
    open(path, "wb").write(text.encode("ascii"))
    return


def run_command(cmd, cwd=None):
    result = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        if result.stdout:
            print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, end="", file=sys.stderr)
        raise RuntimeError("Command failed: {:s}".format(" ".join(cmd)))
    return result.stdout


def run_shell_command(cmd, cwd=None):
    result = subprocess.run(["bash", "-o", "pipefail", "-c", cmd], cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        if result.stdout:
            print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, end="", file=sys.stderr)
        raise RuntimeError("Command failed: {:s}".format(cmd))
    return result.stdout


################################################################################
# utility2


def print_diff(a, b):
    for i, line in enumerate(difflib.unified_diff(a, b, fromfile="before", tofile="after")):
        if i < 2:
            continue
        print(line)
    return


def write_back(context, lines, s, e):
    gef = read_text(context.gef_tmp_path).splitlines()
    gef[s + 1:e] = lines
    write_text(context.gef_tmp_path, "\n".join(gef) + "\n")
    return


################################################################################
# kernel source handling


def ensure_tarball(context):
    kernel = context.kernel
    os.makedirs(kernel.download_dir, exist_ok=True)
    tarball_path = kernel.tarball_path()
    if os.path.exists(tarball_path):
        return tarball_path

    result = subprocess.run([which("wget"), kernel.url, "-O", tarball_path])
    if result.returncode != 0:
        if os.path.exists(tarball_path):
            os.remove(tarball_path)
        raise RuntimeError("Failed to download: {:s}".format(kernel.url))
    return tarball_path


def normalize_tar_member_path(path):
    path = posixpath.normpath(path)
    if path == "." or path.startswith("../") or path.startswith("/"):
        raise RuntimeError("Invalid tar member path: {:s}".format(path))
    return path


def tar_link_target_path(member_path, link_name):
    if posixpath.isabs(link_name):
        raise RuntimeError("Absolute link target is not supported: {:s}".format(link_name))

    member_dir = posixpath.dirname(member_path)
    return normalize_tar_member_path(posixpath.join(member_dir, link_name))


def get_tar_member(tar, member_path):
    try:
        return tar.getmember(member_path)
    except KeyError as err:
        raise RuntimeError("Tar member not found: {:s}".format(member_path)) from err


def get_extract_member_paths(tarball_path, member_path, root_dir):
    member_path = normalize_tar_member_path(member_path)
    root_dir = normalize_tar_member_path(root_dir)
    root_prefix = root_dir + "/"
    member_paths = []
    seen = set()

    with tarfile.open(tarball_path) as tar:
        while True:
            if member_path in seen:
                raise RuntimeError("Tar link loop detected: {:s}".format(member_path))
            seen.add(member_path)

            if member_path != root_dir and not member_path.startswith(root_prefix):
                raise RuntimeError("Link target escapes source tree: {:s}".format(member_path))

            member_paths.append(member_path)
            info = get_tar_member(tar, member_path)
            if not info.issym():
                break

            link_target = tar_link_target_path(member_path, info.linkname)
            print("[+] Following symlink... {:s} -> {:s}".format(member_path, link_target))
            member_path = link_target

    return member_paths


def extract_tar_members(tarball_path, extract_dir, member_paths):
    print("[+] Extracting... {:s}".format(", ".join(member_paths)))
    result = subprocess.run([which("tar"), "xf", tarball_path, "-C", extract_dir] + member_paths)
    if result.returncode != 0:
        raise RuntimeError("Failed to extract: {:s}".format(", ".join(member_paths)))
    return


def ensure_kernel_file(context, filename):
    kernel = context.kernel
    path = kernel.extracted_path(filename)
    if os.path.exists(path):
        return path

    os.makedirs(kernel.extract_dir, exist_ok=True)
    tarball_path = ensure_tarball(context)
    member_path = kernel.member_path(filename)
    member_paths = get_extract_member_paths(tarball_path, member_path, kernel.dirname)
    extract_tar_members(tarball_path, kernel.extract_dir, member_paths)

    if not os.path.exists(path):
        raise RuntimeError("Extracted file not found: {:s}".format(path))
    return path


################################################################################
# update syscall interfaces


def get_new_defs(context, header_path):
    header = ensure_kernel_file(context, header_path)
    cmd = [context.clang_format, "--style={BasedOnStyle: Google, ColumnLimit: 1000}", header]
    syscall_defs = run_command(cmd)
    syscall_defs = [line for line in syscall_defs.splitlines() if line.startswith("asmlinkage")]
    return syscall_defs


def get_gef_defs(context, start_kw, end_kw):
    gef = read_text(context.gef_tmp_path).splitlines()
    try:
        start_kw_pos = gef.index(start_kw)
        end_kw_pos = gef.index(end_kw, start_kw_pos)
    except ValueError as err:
        raise RuntimeError("Failed to find gef.py block: {:s}".format(start_kw)) from err
    return gef[start_kw_pos + 1:end_kw_pos], start_kw_pos, end_kw_pos


def split_arguments(args_text):
    args = []
    current = []
    depth = 0
    for ch in args_text:
        if ch in "([{":
            depth += 1
        elif ch in ")]}" and depth > 0:
            depth -= 1

        if ch == "," and depth == 0:
            args.append("".join(current).strip())
            current = []
            continue
        current.append(ch)

    tail = "".join(current).strip()
    if tail:
        args.append(tail)
    return args


def parse_syscall_def(line):
    result = re.fullmatch(r"(asmlinkage long )(\w+)\((.*)\);(.*)", line)
    if not result:
        return None
    prefix = result.group(1)
    name = result.group(2)
    args = split_arguments(result.group(3))
    suffix = result.group(4)
    return prefix, name, args, suffix


def argument_has_name(arg, name):
    pattern = r"(^|[^A-Za-z0-9_]){:s}\s*(\[[^\]]*\])?$".format(re.escape(name))
    if re.search(pattern, arg):
        return True
    return False


def normalize_argument_type(arg):
    arg = re.sub(r"\*\s*(__user)", r"* \1", arg)
    return arg


def set_argument_type(arg, name, arg_type):
    if argument_has_name(arg, name):
        return "{:s} {:s}".format(arg_type, name)
    return arg_type


def add_argument_name(arg, name):
    if re.search(r"\s\*$", arg):
        return arg + name
    return "{:s} {:s}".format(arg, name)


def apply_line_prefix_rules(line_prefix_rules, line):
    for rule, prefix in line_prefix_rules.items():
        if line.startswith(rule) and not line.startswith(prefix + rule):
            return prefix + line
    return line


def patch_syscall_defs(arg_name_rules, type_text_rules, line_prefix_rules, line_suffix_rules, lines):
    lines_tmp = []
    for line in lines:
        line = apply_line_prefix_rules(line_prefix_rules, line)
        parsed = parse_syscall_def(line)
        if not parsed:
            lines_tmp.append(line)
            continue

        prefix, name, args, suffix = parsed
        changed = False

        if name in arg_name_rules:
            names = arg_name_rules[name]
            if len(args) != len(names):
                print("[!] skip {:s}: unexpected argument count {:d}".format(name, len(args)))
            else:
                args_tmp = []
                for idx, arg in enumerate(args):
                    old_arg = arg
                    arg_name = names[idx]
                    if (name, idx) in type_text_rules:
                        arg = set_argument_type(arg, arg_name, type_text_rules[(name, idx)])
                    else:
                        arg = normalize_argument_type(arg)
                    if not argument_has_name(arg, arg_name):
                        arg = add_argument_name(arg, arg_name)
                    if arg != old_arg:
                        changed = True
                    args_tmp.append(arg)
                args = args_tmp

        if name in line_suffix_rules and suffix != line_suffix_rules[name]:
            suffix = line_suffix_rules[name]
            changed = True

        line = "{:s}{:s}({:s});{:s}".format(prefix, name, ", ".join(args), suffix)
        if changed:
            line = "!" + line
        lines_tmp.append(line)
    return lines_tmp


def syscall_defs_update(context):
    print(titlify("syscall_defs"))

    new_syscall_defs = get_new_defs(context, "include/linux/syscalls.h")
    old_syscall_defs, s, e = get_gef_defs(context, 'syscall_defs = """', '"""')

    arg_name_rules = {
        "sys_io_submit": ["ctx_id", "nr", "iocbpp"],
        "sys_pselect6": ["n", "inp", "outp", "exp", "tsp", "sig"],
        "sys_pselect6_time32": ["n", "inp", "outp", "exp", "tsp", "sig"],
        "sys_ppoll": ["ufds", "nfds", "tsp", "sigmask", "sigsetsize"],
        "sys_ppoll_time32": ["ufds", "nfds", "tsp", "sigmask", "sigsetsize"],
        "sys_rt_sigaction": ["sig", "act", "oact", "sigsetsize"],
        "sys_socket": ["family", "type", "protocol"],
        "sys_socketpair": ["family", "type", "protocol", "usockvec"],
        "sys_bind": ["fd", "umyaddr", "addrlen"],
        "sys_listen": ["fd", "backlog"],
        "sys_accept": ["fd", "upeer_sockaddr", "upeer_addrlen"],
        "sys_connect": ["fd", "uservaddr", "addrlen"],
        "sys_getsockname": ["fd", "usockaddr", "usockaddr_len"],
        "sys_getpeername": ["fd", "usockaddr", "usockaddr_len"],
        "sys_sendto": ["fd", "buff", "len", "flags", "addr", "addr_len"],
        "sys_recvfrom": ["fd", "ubuf", "size", "flags", "addr", "addr_len"],
        "sys_shutdown": ["fd", "how"],
        "sys_accept4": ["fd", "upeer_sockaddr", "upeer_addrlen", "flags"],
    }

    type_text_rules = {
        ("sys_sendto", 3): "unsigned int",
        ("sys_recvfrom", 3): "unsigned int",
    }

    line_prefix_rules = {
        "asmlinkage long sys_clone(": "#",
        "asmlinkage long sys_sigsuspend(int": "#",
        "asmlinkage long sys_ni_syscall(": "#",
        "asmlinkage long sys_fanotify_mark(": "#",
    }

    line_suffix_rules = {}

    new_syscall_defs = patch_syscall_defs(
        arg_name_rules,
        type_text_rules,
        line_prefix_rules,
        line_suffix_rules,
        new_syscall_defs,
    )

    print_diff(old_syscall_defs, new_syscall_defs)
    write_back(context, new_syscall_defs, s, e)
    return


def syscall_defs_compat_update(context):
    print(titlify("syscall_defs_compat"))

    new_syscall_defs = get_new_defs(context, "include/linux/compat.h")
    old_syscall_defs, s, e = get_gef_defs(context, 'syscall_defs_compat = """', '"""')

    arg_name_rules = {
        "compat_sys_waitid": ["which", "pid", "waitid", "options", "uru"],
        "compat_sys_kexec_load": ["entry", "nr_segments", "segments", "flags"],
        "compat_sys_rt_sigaction": ["sig", "act", "oact", "sigsetsize"],
        "compat_sys_fanotify_mark": ["fanotify_fd", "flags", "mask_1", "mask_2", "dfd", "pathname"],
    }

    type_text_rules = {}

    line_prefix_rules = {}

    line_suffix_rules = {
        "compat_sys_io_pgetevents": " # codespell:ignore",
        "compat_sys_io_pgetevents_time64": " # codespell:ignore",
    }

    new_syscall_defs = patch_syscall_defs(
        arg_name_rules,
        type_text_rules,
        line_prefix_rules,
        line_suffix_rules,
        new_syscall_defs,
    )

    print_diff(old_syscall_defs, new_syscall_defs)
    write_back(context, new_syscall_defs, s, e)
    return


################################################################################
# update syscall table


def get_new_tbl(context, tbl_path):
    path = ensure_kernel_file(context, tbl_path)
    print("[+] path:", path)
    new_tbl = read_text(path).expandtabs(8).splitlines()
    new_tbl = [l for l in new_tbl if l and not l.startswith("#")]
    return new_tbl


def get_new_tbl_by_cmds(context, cmds, required_paths):
    for path in required_paths:
        ensure_kernel_file(context, path)
    cmds = "; ".join([cmd.lstrip() for cmd in cmds.splitlines() if cmd])
    print("[+] cmds:", cmds)
    result = run_shell_command(cmds)
    return result.splitlines()


def x64_syscall_tbl_update(context):
    print(titlify("x64_syscall_tbl"))
    new_tbl = get_new_tbl(context, "arch/x86/entry/syscalls/syscall_64.tbl")
    old_tbl, s, e = get_gef_defs(context, 'x64_syscall_tbl = """', '"""')
    print_diff(old_tbl, new_tbl)
    write_back(context, new_tbl, s, e)
    return


def i386_syscall_tbl_update(context):
    print(titlify("i386_syscall_tbl"))
    new_tbl = get_new_tbl(context, "arch/x86/entry/syscalls/syscall_32.tbl")
    old_tbl, s, e = get_gef_defs(context, 'x86_syscall_tbl = """', '"""')
    print_diff(old_tbl, new_tbl)
    write_back(context, new_tbl, s, e)
    return


def arm64_syscall_tbl_update(context):
    print(titlify("arm64_syscall_tbl"))
    new_tbl = get_new_tbl(context, "arch/arm64/tools/syscall_64.tbl")
    old_tbl, s, e = get_gef_defs(context, 'arm64_syscall_tbl = """', '"""')
    print_diff(old_tbl, new_tbl)
    write_back(context, new_tbl, s, e)
    return


def arm_compat_syscall_tbl_update(context):
    print(titlify("arm_compat_syscall_tbl"))
    new_tbl = get_new_tbl(context, "arch/arm64/tools/syscall_32.tbl")
    old_tbl, s, e = get_gef_defs(context, 'arm_compat_syscall_tbl = """', '"""')
    print_diff(old_tbl, new_tbl)
    write_back(context, new_tbl, s, e)
    return


def arm_native_syscall_tbl_update(context):
    print(titlify("arm_native_syscall_tbl"))
    new_tbl = get_new_tbl(context, "arch/arm/tools/syscall.tbl")
    old_tbl, s, e = get_gef_defs(context, 'arm_native_syscall_tbl = """', '"""')
    print_diff(old_tbl, new_tbl)
    write_back(context, new_tbl, s, e)
    return


def mips_o32_syscall_tbl_update(context):
    print(titlify("mips_o32_syscall_tbl"))
    new_tbl = get_new_tbl(context, "arch/mips/kernel/syscalls/syscall_o32.tbl")
    old_tbl, s, e = get_gef_defs(context, 'mips_o32_syscall_tbl = """', '"""')
    print_diff(old_tbl, new_tbl)
    write_back(context, new_tbl, s, e)
    return


def mips_n32_syscall_tbl_update(context):
    print(titlify("mips_n32_syscall_tbl"))
    new_tbl = get_new_tbl(context, "arch/mips/kernel/syscalls/syscall_n32.tbl")
    old_tbl, s, e = get_gef_defs(context, 'mips_n32_syscall_tbl = """', '"""')
    print_diff(old_tbl, new_tbl)
    write_back(context, new_tbl, s, e)
    return


def mips_n64_syscall_tbl_update(context):
    print(titlify("mips_n64_syscall_tbl"))
    new_tbl = get_new_tbl(context, "arch/mips/kernel/syscalls/syscall_n64.tbl")
    old_tbl, s, e = get_gef_defs(context, 'mips_n64_syscall_tbl = """', '"""')
    print_diff(old_tbl, new_tbl)
    write_back(context, new_tbl, s, e)
    return


def ppc_syscall_tbl_update(context):
    print(titlify("ppc_syscall_tbl"))
    new_tbl = get_new_tbl(context, "arch/powerpc/kernel/syscalls/syscall.tbl")
    old_tbl, s, e = get_gef_defs(context, 'ppc_syscall_tbl = """', '"""')
    print_diff(old_tbl, new_tbl)
    write_back(context, new_tbl, s, e)
    return


def sparc_syscall_tbl_update(context):
    print(titlify("sparc_syscall_tbl"))
    new_tbl = get_new_tbl(context, "arch/sparc/kernel/syscalls/syscall.tbl")
    old_tbl, s, e = get_gef_defs(context, 'sparc_syscall_tbl = """', '"""')
    print_diff(old_tbl, new_tbl)
    write_back(context, new_tbl, s, e)
    return


def riscv64_syscall_tbl_update(context):
    print(titlify("riscv64_syscall_tbl"))
    print("\033[1m" + "[!] same with arm64 \033[0m")
    return


def riscv32_syscall_tbl_update(context):
    print(titlify("riscv32_syscall_tbl"))
    print("\033[1m" + "[!] same with arm64 \033[0m")
    return


def s390x_syscall_tbl_update(context):
    print(titlify("s390x_syscall_tbl"))
    new_tbl = get_new_tbl(context, "arch/s390/kernel/syscalls/syscall.tbl")
    old_tbl, s, e = get_gef_defs(context, 's390x_syscall_tbl = """', '"""')
    print_diff(old_tbl, new_tbl)
    write_back(context, new_tbl, s, e)
    return


def sh4_syscall_tbl_update(context):
    print(titlify("sh4_syscall_tbl"))
    new_tbl = get_new_tbl(context, "arch/sh/kernel/syscalls/syscall.tbl")
    old_tbl, s, e = get_gef_defs(context, 'sh4_syscall_tbl = """', '"""')
    print_diff(old_tbl, new_tbl)
    write_back(context, new_tbl, s, e)
    return


def m68k_syscall_tbl_update(context):
    print(titlify("m68k_syscall_tbl"))
    new_tbl = get_new_tbl(context, "arch/m68k/kernel/syscalls/syscall.tbl")
    old_tbl, s, e = get_gef_defs(context, 'm68k_syscall_tbl = """', '"""')
    print_diff(old_tbl, new_tbl)
    write_back(context, new_tbl, s, e)
    return


def alpha_syscall_tbl_update(context):
    print(titlify("alpha_syscall_tbl"))
    new_tbl = get_new_tbl(context, "arch/alpha/kernel/syscalls/syscall.tbl")
    old_tbl, s, e = get_gef_defs(context, 'alpha_syscall_tbl = """', '"""')
    print_diff(old_tbl, new_tbl)
    write_back(context, new_tbl, s, e)
    return


def hppa_syscall_tbl_update(context):
    print(titlify("hppa_syscall_tbl"))
    new_tbl = get_new_tbl(context, "arch/parisc/kernel/syscalls/syscall.tbl")
    old_tbl, s, e = get_gef_defs(context, 'hppa_syscall_tbl = """', '"""')
    print_diff(old_tbl, new_tbl)
    write_back(context, new_tbl, s, e)
    return


def or1k_syscall_tbl_update(context):
    print(titlify("or1k_syscall_tbl"))
    print("\033[1m" + "[!] same with arm64 \033[0m")
    return


def nios2_syscall_tbl_update(context):
    print(titlify("nios2_syscall_tbl"))
    print("\033[1m" + "[!] same with arm64 \033[0m")
    return


def microblaze_syscall_tbl_update(context):
    print(titlify("microblaze_syscall_tbl"))
    new_tbl = get_new_tbl(context, "arch/microblaze/kernel/syscalls/syscall.tbl")
    old_tbl, s, e = get_gef_defs(context, 'microblaze_syscall_tbl = """', '"""')
    print_diff(old_tbl, new_tbl)
    write_back(context, new_tbl, s, e)
    return


def xtensa_syscall_tbl_update(context):
    print(titlify("xtensa_syscall_tbl"))
    new_tbl = get_new_tbl(context, "arch/xtensa/kernel/syscalls/syscall.tbl")
    old_tbl, s, e = get_gef_defs(context, 'xtensa_syscall_tbl = """', '"""')
    print_diff(old_tbl, new_tbl)
    write_back(context, new_tbl, s, e)
    return


def cris_syscall_tbl_update(context):
    print(titlify("cris_syscall_tbl"))
    new_tbl = get_new_tbl_by_cmds(
        context,
        r"""
        cd {:s}
        awk '/sys_call_table:/,/^$/' arch/cris/arch-v10/kernel/entry.S | grep -o "\.long \w*" | nl -v0 | awk '{{print $1" cris "substr($3,5)" "$3}}' |column -t
        """.format(context.kernel.source_dir()),
        ["arch/cris/arch-v10/kernel/entry.S"],
    )
    old_tbl, s, e = get_gef_defs(context, 'cris_syscall_tbl = """', '"""')
    print_diff(old_tbl, new_tbl)
    write_back(context, new_tbl, s, e)
    return


def loongarch_syscall_tbl_update(context):
    print(titlify("loongarch_syscall_tbl"))
    print("\033[1m" + "[!] skip loongarch_syscall_tbl. need fix manually." + "\033[0m")
    return

    new_tbl = get_new_tbl_by_cmds(
        context,
        r"""
        cd {:s}
        gcc -I `pwd`/include/uapi/ -E -D__SYSCALL=SYSCALL arch/loongarch/include/uapi/asm/unistd.h | grep ^SYSCALL | sed -e 's/SYSCALL(//;s/[,)]//g' > {:s}
        grep -oP "__NR\S+\s+\d+$" include/uapi/asm-generic/unistd.h | grep -v __NR_sync_file_range2 > {:s}
        join -2 2 -o 1.1,1.10,2.1,1.2 -e loongarch {:s} {:s} 2>/dev/null | sed -e 's/\(__NR_\|__NR3264_\)//g' | column -t
        """.format(context.kernel.source_dir(), context.tmp_a, context.tmp_b, context.tmp_a, context.tmp_b),
        [
            "arch/loongarch/include/uapi/asm/unistd.h",
            "include/uapi/asm-generic/unistd.h",
        ],
    )
    old_tbl, s, e = get_gef_defs(context, 'loongarch_syscall_tbl = """', '"""')
    print_diff(old_tbl, new_tbl)
    write_back(context, new_tbl, s, e)
    return


def arc_syscall_tbl_update(context):
    print(titlify("arc_syscall_tbl"))
    print("\033[1m" + "[!] same with arm64 \033[0m")
    return


def csky_syscall_tbl_update(context):
    print(titlify("csky_syscall_tbl"))
    print("\033[1m" + "[!] same with arm64 \033[0m")
    return


################################################################################
# main


def main():
    args = parse_args()

    try:
        with tempfile.TemporaryDirectory(prefix="gef-update-syscalls-") as work_dir:
            context = init_context(args, work_dir)

            syscall_defs_update(context)
            syscall_defs_compat_update(context)

            x64_syscall_tbl_update(context)
            i386_syscall_tbl_update(context)
            arm64_syscall_tbl_update(context)
            arm_compat_syscall_tbl_update(context)
            arm_native_syscall_tbl_update(context)
            mips_o32_syscall_tbl_update(context)
            mips_n32_syscall_tbl_update(context)
            mips_n64_syscall_tbl_update(context)
            ppc_syscall_tbl_update(context)
            sparc_syscall_tbl_update(context)
            riscv64_syscall_tbl_update(context)
            riscv32_syscall_tbl_update(context)
            s390x_syscall_tbl_update(context)
            sh4_syscall_tbl_update(context)
            m68k_syscall_tbl_update(context)
            alpha_syscall_tbl_update(context)
            hppa_syscall_tbl_update(context)
            or1k_syscall_tbl_update(context)
            nios2_syscall_tbl_update(context)
            microblaze_syscall_tbl_update(context)
            xtensa_syscall_tbl_update(context)
            #cris_syscall_tbl_update(context) # cris is removed at current linux
            loongarch_syscall_tbl_update(context) # skip
            arc_syscall_tbl_update(context)
            csky_syscall_tbl_update(context)

            print_patch_result(context)
    except Exception as err:
        print("[-] {:s}".format(str(err)), file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    main()
