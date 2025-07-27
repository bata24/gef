#!/usr/bin/python
import sys
import os
import subprocess
import shutil
import hashlib

################################################################################
# init and arguments check

def init():
    if len(sys.argv) != 3:
        print("usage: {:s} KERNEL_SRC_DIR GEF_DIR".format(sys.argv[0]))
        print()
        print("example: {:s} /tmp/work/linux-6.6-rc7 /tmp/work/gef".format(sys.argv[0]))
        exit()

    which("clang-format")

    global K_DIR, GEF_DIR, GEF_PATH, GEF_TMP_PATH
    K_DIR = sys.argv[1]
    GEF_DIR = sys.argv[2]
    GEF_PATH = os.path.join(sys.argv[2], "gef.py")
    GEF_TMP_PATH = GEF_PATH + ".tmp"

    if not os.path.exists(K_DIR):
        print("[-] Not found {:s}".format(K_DIR))
        exit()

    if not os.path.exists(GEF_PATH):
        print("[-] Not found {:s}".format(GEF_PATH))
        exit()

    if os.path.exists(GEF_TMP_PATH):
        print("[-] Found {:s} already.".format(GEF_TMP_PATH))
        exit()

    if os.path.exists("/tmp/a"):
        print("[-] Found {:s} already.".format("/tmp/a"))
        exit()

    if os.path.exists("/tmp/b"):
        print("[-] Found {:s} already.".format("/tmp/b"))
        exit()

    shutil.copyfile(GEF_PATH, GEF_TMP_PATH)
    return

def print_patch_result():
    print(titlify("patch result"))
    h1 = hashlib.sha1(open(GEF_PATH, "rb").read()).hexdigest()
    h2 = hashlib.sha1(open(GEF_TMP_PATH, "rb").read()).hexdigest()
    if h1 != h2:
        print("[+] patched gef.py is saved to {:s}".format(GEF_TMP_PATH))
    else:
        print("[+] No diff")
        os.unlink(GEF_TMP_PATH)
    return

def cleanup():
    if os.path.exists("/tmp/a"):
        os.unlink("/tmp/a")
    if os.path.exists("/tmp/b"):
        os.unlink("/tmp/b")
    return

################################################################################
# utility

def get_terminal_size():
    import termios
    import struct
    import fcntl
    try:
        tty_rows, tty_columns = struct.unpack("hh", fcntl.ioctl(1, termios.TIOCGWINSZ, "1234"))
        return tty_rows, tty_columns
    except OSError:
        return 600, 100

def titlify(text):
    cols = get_terminal_size()[1]
    cs = "\033[36m" # cyan
    ce = "\033[0m" # normal

    msg = []
    if text:
        nb = (cols - len(text) - 2) // 2
        msg.append(cs + "{} ".format("-" * nb) + ce)
        msg.append(cs + text + ce)
        msg.append(cs + " {}".format("-" * nb) + ce)
    else:
        msg.append(cs + "{}".format("-" * cols) + ce)
    return "".join(msg)

def which(command):
    x = subprocess.getoutput("which {:s}".format(command))
    if not x:
        print("[-] Not found {:s}".format(command))
        exit()
    return x

def str2bytes(x):
    if isinstance(x, bytes):
        return x
    if isinstance(x, str):
        x = bytes(ord(xx) for xx in x)
        return x
    raise

def bytes2str(x):
    if isinstance(x, str):
        return x
    if isinstance(x, bytes):
        x = "".join(chr(xx) for xx in x)
        return x
    raise

################################################################################
# utility2

def print_diff(a, b):
    import difflib
    for i, line in enumerate(difflib.unified_diff(a, b, fromfile="before", tofile="after")):
        if i < 2:
            continue
        print(line)
    return

def write_back(lines, s, e):
    gef = open(GEF_TMP_PATH, "rb").read().decode("ascii").splitlines()
    gef[s + 1:e] = lines
    open(GEF_TMP_PATH, "wb").write(("\n".join(gef) + "\n").encode())
    return

################################################################################
# update syscall interfaces

def get_new_defs(header_path):
    clang = which("clang-format")
    header = os.path.join(K_DIR, header_path)
    cmd = "{:s} --style='{{BasedOnStyle: Google, ColumnLimit: 1000}}' {:s}".format(clang, header)
    syscall_defs = subprocess.getoutput(cmd)
    syscall_defs = [line for line in syscall_defs.splitlines() if line.startswith("asmlinkage")]
    return syscall_defs

def get_gef_defs(start_kw, end_kw):
    gef = open(GEF_TMP_PATH, "rb").read().decode("ascii").splitlines()
    start_kw_pos = gef.index(start_kw)
    end_kw_pos = gef.index(end_kw, start_kw_pos)
    return gef[start_kw_pos + 1:end_kw_pos], start_kw_pos, end_kw_pos

# replace line and add "!"
def replace_lines1(replace_rules, lines):
    for rule in replace_rules:
        before, after = rule
        if before not in lines:
            continue
        idx = lines.index(before)
        lines[idx] = "!" + after
    return lines

# add "#"
def replace_lines2(replace_rules, lines):
    for rule in replace_rules:
        lines_tmp = []
        for line in lines:
            if line.startswith(rule):
                line = "#" + line
            lines_tmp.append(line)
        lines = lines_tmp[::]
    return lines

def syscall_defs_update():
    print(titlify("syscall_defs"))

    new_syscall_defs = get_new_defs("include/linux/syscalls.h")
    old_syscall_defs, s, e = get_gef_defs('syscall_defs = """', '"""')

    # replace some defs
    replace_rules1 = [
        ["asmlinkage long sys_io_submit(aio_context_t, long, struct iocb __user *__user *);",
         "asmlinkage long sys_io_submit(aio_context_t ctx_id, long nr, struct iocb __user * __user *iocbpp);",
        ],
        ["asmlinkage long sys_pselect6(int, fd_set __user *, fd_set __user *, fd_set __user *, struct __kernel_timespec __user *, void __user *);",
         "asmlinkage long sys_pselect6(int n, fd_set __user *inp, fd_set __user *outp, fd_set __user *exp, struct __kernel_timespec __user *tsp, void __user *sig);",
        ],
        ["asmlinkage long sys_pselect6_time32(int, fd_set __user *, fd_set __user *, fd_set __user *, struct old_timespec32 __user *, void __user *);",
         "asmlinkage long sys_pselect6_time32(int n, fd_set __user *inp, fd_set __user *outp, fd_set __user *exp, struct old_timespec32 __user *tsp, void __user *sig);",
        ],
        ["asmlinkage long sys_ppoll(struct pollfd __user *, unsigned int, struct __kernel_timespec __user *, const sigset_t __user *, size_t);",
         "asmlinkage long sys_ppoll(struct pollfd __user *ufds, unsigned int nfds, struct __kernel_timespec __user *tsp, const sigset_t __user *sigmask, size_t sigsetsize);",
        ],
        ["asmlinkage long sys_ppoll_time32(struct pollfd __user *, unsigned int, struct old_timespec32 __user *, const sigset_t __user *, size_t);",
         "asmlinkage long sys_ppoll_time32(struct pollfd __user *ufds, unsigned int nfds, struct old_timespec32 __user *tsp, const sigset_t __user *sigmask, size_t sigsetsize);",
        ],
        ["asmlinkage long sys_rt_sigaction(int, const struct sigaction __user *, struct sigaction __user *, size_t);",
         "asmlinkage long sys_rt_sigaction(int sig, const struct sigaction __user *act, struct sigaction __user *oact, size_t sigsetsize);",
        ],
        ["asmlinkage long sys_socket(int, int, int);",
         "asmlinkage long sys_socket(int family, int type, int protocol);",
        ],
        ["asmlinkage long sys_socketpair(int, int, int, int __user *);",
         "asmlinkage long sys_socketpair(int family, int type, int protocol, int __user *usockvec);",
        ],
        ["asmlinkage long sys_bind(int, struct sockaddr __user *, int);",
         "asmlinkage long sys_bind(int fd, struct sockaddr __user *umyaddr, int addrlen);",
        ],
        ["asmlinkage long sys_listen(int, int);",
         "asmlinkage long sys_listen(int fd, int backlog);",
        ],
        ["asmlinkage long sys_accept(int, struct sockaddr __user *, int __user *);",
         "asmlinkage long sys_accept(int fd, struct sockaddr __user *upeer_sockaddr, int __user *upeer_addrlen);",
        ],
        ["asmlinkage long sys_connect(int, struct sockaddr __user *, int);",
         "asmlinkage long sys_connect(int fd, struct sockaddr __user *uservaddr, int addrlen);",
        ],
        ["asmlinkage long sys_getsockname(int, struct sockaddr __user *, int __user *);",
         "asmlinkage long sys_getsockname(int fd, struct sockaddr __user *usockaddr, int __user *usockaddr_len);",
        ],
        ["asmlinkage long sys_getpeername(int, struct sockaddr __user *, int __user *);",
         "asmlinkage long sys_getpeername(int fd, struct sockaddr __user *usockaddr, int __user *usockaddr_len);",
        ],
        ["asmlinkage long sys_sendto(int, void __user *, size_t, unsigned, struct sockaddr __user *, int);",
         "asmlinkage long sys_sendto(int fd, void __user *buff, size_t len, unsigned int flags, struct sockaddr __user *addr, int addr_len);",
        ],
        ["asmlinkage long sys_recvfrom(int, void __user *, size_t, unsigned, struct sockaddr __user *, int __user *);",
         "asmlinkage long sys_recvfrom(int fd, void __user *ubuf, size_t size, unsigned int flags, struct sockaddr __user *addr, int __user *addr_len);",
        ],
        ["asmlinkage long sys_shutdown(int, int);",
         "asmlinkage long sys_shutdown(int fd, int how);",
        ],
        ["asmlinkage long sys_accept4(int, struct sockaddr __user *, int __user *, int);",
         "asmlinkage long sys_accept4(int fd, struct sockaddr __user *upeer_sockaddr, int __user *upeer_addrlen, int flags);",
        ],
    ]

    replace_rules2 = [
        "asmlinkage long sys_clone(",
        "asmlinkage long sys_sigsuspend(int",
        "asmlinkage long sys_ni_syscall(",
        "asmlinkage long sys_fanotify_mark(",
    ]

    new_syscall_defs = replace_lines1(replace_rules1, new_syscall_defs)
    new_syscall_defs = replace_lines2(replace_rules2, new_syscall_defs)

    print_diff(old_syscall_defs, new_syscall_defs)
    write_back(new_syscall_defs, s, e)
    return

def syscall_defs_compat_update():
    print(titlify("syscall_defs_compat"))

    new_syscall_defs = get_new_defs("include/linux/compat.h")
    old_syscall_defs, s, e = get_gef_defs('syscall_defs_compat = """', '"""')

    replace_rules1 = [
        ["asmlinkage long compat_sys_waitid(int, compat_pid_t, struct compat_siginfo __user *, int, struct compat_rusage __user *);",
         "asmlinkage long compat_sys_waitid(int which, compat_pid_t pid, struct compat_siginfo __user *waitid, int options, struct compat_rusage __user *uru);",
        ],
        ["asmlinkage long compat_sys_kexec_load(compat_ulong_t entry, compat_ulong_t nr_segments, struct compat_kexec_segment __user *, compat_ulong_t flags);",
         "asmlinkage long compat_sys_kexec_load(compat_ulong_t entry, compat_ulong_t nr_segments, struct compat_kexec_segment __user *segments, compat_ulong_t flags);",
        ],
        ["asmlinkage long compat_sys_rt_sigaction(int, const struct compat_sigaction __user *, struct compat_sigaction __user *, compat_size_t);",
         "asmlinkage long compat_sys_rt_sigaction(int sig, const struct compat_sigaction __user *act, struct compat_sigaction __user *oact, compat_size_t sigsetsize);",
        ],
        ["asmlinkage long compat_sys_fanotify_mark(int, unsigned int, __u32, __u32, int, const char __user *);",
         "asmlinkage long compat_sys_fanotify_mark(int fanotify_fd, unsigned int flags, __u32 mask_1, __u32 mask_2, int dfd, const char __user *pathname);",
        ],
        ["asmlinkage long compat_sys_io_pgetevents(compat_aio_context_t ctx_id, compat_long_t min_nr, compat_long_t nr, struct io_event __user *events, struct old_timespec32 __user *timeout, const struct __compat_aio_sigset __user *usig);",
         "asmlinkage long compat_sys_io_pgetevents(compat_aio_context_t ctx_id, compat_long_t min_nr, compat_long_t nr, struct io_event __user *events, struct old_timespec32 __user *timeout, const struct __compat_aio_sigset __user *usig); # codespell:ignore",
        ],
        ["asmlinkage long compat_sys_io_pgetevents_time64(compat_aio_context_t ctx_id, compat_long_t min_nr, compat_long_t nr, struct io_event __user *events, struct __kernel_timespec __user *timeout, const struct __compat_aio_sigset __user *usig);",
         "asmlinkage long compat_sys_io_pgetevents_time64(compat_aio_context_t ctx_id, compat_long_t min_nr, compat_long_t nr, struct io_event __user *events, struct __kernel_timespec __user *timeout, const struct __compat_aio_sigset __user *usig); # codespell:ignore",
        ],
    ]

    replace_rules2 = [
    ]

    new_syscall_defs = replace_lines1(replace_rules1, new_syscall_defs)
    new_syscall_defs = replace_lines2(replace_rules2, new_syscall_defs)

    print_diff(old_syscall_defs, new_syscall_defs)
    write_back(new_syscall_defs, s, e)
    return

################################################################################
# update syscall table

def get_new_tbl(tbl_path):
    path = os.path.join(K_DIR, tbl_path)
    print("[+] path:", path)
    new_tbl = open(path, "rb").read().decode("ascii").expandtabs(8).splitlines()
    new_tbl = [l for l in new_tbl if l and not l.startswith("#")]
    return new_tbl

def get_new_tbl_by_cmds(cmds):
    cmds = "; ".join([cmd.lstrip() for cmd in cmds.splitlines() if cmd])
    print("[+] cmds:", cmds)
    result = subprocess.getoutput(cmds)
    return result.splitlines()

def x64_syscall_tbl_update():
    print(titlify(sys._getframe().f_code.co_name[:-7]))
    new_tbl = get_new_tbl("arch/x86/entry/syscalls/syscall_64.tbl")
    old_tbl, s, e = get_gef_defs('x64_syscall_tbl = """', '"""')
    print_diff(old_tbl, new_tbl)
    write_back(new_tbl, s, e)
    return

def i386_syscall_tbl_update():
    print(titlify(sys._getframe().f_code.co_name[:-7]))
    new_tbl = get_new_tbl("arch/x86/entry/syscalls/syscall_32.tbl")
    old_tbl, s, e = get_gef_defs('x86_syscall_tbl = """', '"""')
    print_diff(old_tbl, new_tbl)
    write_back(new_tbl, s, e)
    return

def arm64_syscall_tbl_update():
    print(titlify(sys._getframe().f_code.co_name[:-7]))
    new_tbl = get_new_tbl("arch/arm64/tools/syscall_64.tbl")
    old_tbl, s, e = get_gef_defs('arm64_syscall_tbl = """', '"""')
    print_diff(old_tbl, new_tbl)
    write_back(new_tbl, s, e)
    return

def arm_compat_syscall_tbl_update():
    print(titlify(sys._getframe().f_code.co_name[:-7]))
    new_tbl = get_new_tbl("arch/arm64/tools/syscall_32.tbl")
    old_tbl, s, e = get_gef_defs('arm_compat_syscall_tbl = """', '"""')
    print_diff(old_tbl, new_tbl)
    write_back(new_tbl, s, e)
    return

def arm_native_syscall_tbl_update():
    print(titlify(sys._getframe().f_code.co_name[:-7]))
    new_tbl = get_new_tbl("arch/arm/tools/syscall.tbl")
    old_tbl, s, e = get_gef_defs('arm_native_syscall_tbl = """', '"""')
    print_diff(old_tbl, new_tbl)
    write_back(new_tbl, s, e)
    return

def mips_o32_syscall_tbl_update():
    print(titlify(sys._getframe().f_code.co_name[:-7]))
    new_tbl = get_new_tbl("arch/mips/kernel/syscalls/syscall_o32.tbl")
    old_tbl, s, e = get_gef_defs('mips_o32_syscall_tbl = """', '"""')
    print_diff(old_tbl, new_tbl)
    write_back(new_tbl, s, e)
    return

def mips_n32_syscall_tbl_update():
    print(titlify(sys._getframe().f_code.co_name[:-7]))
    new_tbl = get_new_tbl("arch/mips/kernel/syscalls/syscall_n32.tbl")
    old_tbl, s, e = get_gef_defs('mips_n32_syscall_tbl = """', '"""')
    print_diff(old_tbl, new_tbl)
    write_back(new_tbl, s, e)
    return

def mips_n64_syscall_tbl_update():
    print(titlify(sys._getframe().f_code.co_name[:-7]))
    new_tbl = get_new_tbl("arch/mips/kernel/syscalls/syscall_n64.tbl")
    old_tbl, s, e = get_gef_defs('mips_n64_syscall_tbl = """', '"""')
    print_diff(old_tbl, new_tbl)
    write_back(new_tbl, s, e)
    return

def ppc_syscall_tbl_update():
    print(titlify(sys._getframe().f_code.co_name[:-7]))
    new_tbl = get_new_tbl("arch/powerpc/kernel/syscalls/syscall.tbl")
    old_tbl, s, e = get_gef_defs('ppc_syscall_tbl = """', '"""')
    print_diff(old_tbl, new_tbl)
    write_back(new_tbl, s, e)
    return

def sparc_syscall_tbl_update():
    print(titlify(sys._getframe().f_code.co_name[:-7]))
    new_tbl = get_new_tbl("arch/sparc/kernel/syscalls/syscall.tbl")
    old_tbl, s, e = get_gef_defs('sparc_syscall_tbl = """', '"""')
    print_diff(old_tbl, new_tbl)
    write_back(new_tbl, s, e)
    return

def riscv64_syscall_tbl_update():
    print(titlify(sys._getframe().f_code.co_name[:-7]))
    print("\033[1m" + "[!] same with arm64 \033[0m")
    return

def riscv32_syscall_tbl_update():
    print(titlify(sys._getframe().f_code.co_name[:-7]))
    print("\033[1m" + "[!] same with arm64 \033[0m")
    return

def s390x_syscall_tbl_update():
    print(titlify(sys._getframe().f_code.co_name[:-7]))
    new_tbl = get_new_tbl("arch/s390/kernel/syscalls/syscall.tbl")
    old_tbl, s, e = get_gef_defs('s390x_syscall_tbl = """', '"""')
    print_diff(old_tbl, new_tbl)
    write_back(new_tbl, s, e)
    return

def sh4_syscall_tbl_update():
    print(titlify(sys._getframe().f_code.co_name[:-7]))
    new_tbl = get_new_tbl("arch/sh/kernel/syscalls/syscall.tbl")
    old_tbl, s, e = get_gef_defs('sh4_syscall_tbl = """', '"""')
    print_diff(old_tbl, new_tbl)
    write_back(new_tbl, s, e)
    return

def m68k_syscall_tbl_update():
    print(titlify(sys._getframe().f_code.co_name[:-7]))
    new_tbl = get_new_tbl("arch/m68k/kernel/syscalls/syscall.tbl")
    old_tbl, s, e = get_gef_defs('m68k_syscall_tbl = """', '"""')
    print_diff(old_tbl, new_tbl)
    write_back(new_tbl, s, e)
    return

def alpha_syscall_tbl_update():
    print(titlify(sys._getframe().f_code.co_name[:-7]))
    new_tbl = get_new_tbl("arch/alpha/kernel/syscalls/syscall.tbl")
    old_tbl, s, e = get_gef_defs('alpha_syscall_tbl = """', '"""')
    print_diff(old_tbl, new_tbl)
    write_back(new_tbl, s, e)
    return

def hppa_syscall_tbl_update():
    print(titlify(sys._getframe().f_code.co_name[:-7]))
    new_tbl = get_new_tbl("arch/parisc/kernel/syscalls/syscall.tbl")
    old_tbl, s, e = get_gef_defs('hppa_syscall_tbl = """', '"""')
    print_diff(old_tbl, new_tbl)
    write_back(new_tbl, s, e)
    return

def or1k_syscall_tbl_update():
    print(titlify(sys._getframe().f_code.co_name[:-7]))
    print("\033[1m" + "[!] same with arm64 \033[0m")
    return

def nios2_syscall_tbl_update():
    print(titlify(sys._getframe().f_code.co_name[:-7]))
    print("\033[1m" + "[!] same with arm64 \033[0m")
    return

def microblaze_syscall_tbl_update():
    print(titlify(sys._getframe().f_code.co_name[:-7]))
    new_tbl = get_new_tbl("arch/microblaze/kernel/syscalls/syscall.tbl")
    old_tbl, s, e = get_gef_defs('microblaze_syscall_tbl = """', '"""')
    print_diff(old_tbl, new_tbl)
    write_back(new_tbl, s, e)
    return

def xtensa_syscall_tbl_update():
    print(titlify(sys._getframe().f_code.co_name[:-7]))
    new_tbl = get_new_tbl("arch/xtensa/kernel/syscalls/syscall.tbl")
    old_tbl, s, e = get_gef_defs('xtensa_syscall_tbl = """', '"""')
    print_diff(old_tbl, new_tbl)
    write_back(new_tbl, s, e)
    return

def cris_syscall_tbl_update():
    print(titlify(sys._getframe().f_code.co_name[:-7]))
    new_tbl = get_new_tbl_by_cmds(
        r"""
        cd {:s}
        awk '/sys_call_table:/,/^$/' arch/cris/arch-v10/kernel/entry.S | grep -o "\.long \w*" | nl -v0 | awk '{print $1" cris "substr($3,5)" "$3}' |column -t
        """.format(K_DIR)
    )
    old_tbl, s, e = get_gef_defs('cris_syscall_tbl = """', '"""')
    print_diff(old_tbl, new_tbl)
    write_back(new_tbl, s, e)
    return

def loongarch_syscall_tbl_update():
    print(titlify(sys._getframe().f_code.co_name[:-7]))
    print("\033[1m" + "[!] skip {:s}. need fix manually.".format(sys._getframe().f_code.co_name[:-19]) + "\033[0m")
    return

    new_tbl = get_new_tbl_by_cmds(
        r"""
        cd {:s}
        gcc -I `pwd`/include/uapi/ -E -D__SYSCALL=SYSCALL arch/loongarch/include/uapi/asm/unistd.h | grep ^SYSCALL | sed -e 's/SYSCALL(//;s/[,)]//g' > /tmp/a
        grep -oP "__NR\S+\s+\d+$" include/uapi/asm-generic/unistd.h | grep -v __NR_sync_file_range2 > /tmp/b
        join -2 2 -o 1.1,1.10,2.1,1.2 -e loongarch /tmp/a /tmp/b 2>/dev/null | sed -e 's/\(__NR_\|__NR3264_\)//g' | column -t
        """.format(K_DIR)
    )
    old_tbl, s, e = get_gef_defs('loongarch_syscall_tbl = """', '"""')
    print_diff(old_tbl, new_tbl)
    write_back(new_tbl, s, e)
    return

def arc_syscall_tbl_update():
    print(titlify(sys._getframe().f_code.co_name[:-7]))
    print("\033[1m" + "[!] same with arm64 \033[0m")
    return

def csky_syscall_tbl_update():
    print(titlify(sys._getframe().f_code.co_name[:-7]))
    print("\033[1m" + "[!] same with arm64 \033[0m")
    return

################################################################################
# main

if __name__ == "__main__":
    init()

    syscall_defs_update()
    syscall_defs_compat_update()

    x64_syscall_tbl_update()
    i386_syscall_tbl_update()
    arm64_syscall_tbl_update()
    arm_compat_syscall_tbl_update()
    arm_native_syscall_tbl_update()
    mips_o32_syscall_tbl_update()
    mips_n32_syscall_tbl_update()
    mips_n64_syscall_tbl_update()
    ppc_syscall_tbl_update()
    sparc_syscall_tbl_update()
    riscv64_syscall_tbl_update()
    riscv32_syscall_tbl_update()
    s390x_syscall_tbl_update()
    sh4_syscall_tbl_update()
    m68k_syscall_tbl_update()
    alpha_syscall_tbl_update()
    hppa_syscall_tbl_update()
    or1k_syscall_tbl_update()
    nios2_syscall_tbl_update()
    microblaze_syscall_tbl_update()
    xtensa_syscall_tbl_update()
    #cris_syscall_tbl_update() # cris is removed at current linux
    loongarch_syscall_tbl_update() # skip
    arc_syscall_tbl_update()
    csky_syscall_tbl_update()

    print_patch_result()
    cleanup()
