## Table of Contents
* [What is this?](#what-is-this)
* [Setup](#setup)
    * [Install](#install)
    * [Install (Ubuntu 23.04)](#install-ubuntu-2304)
    * [Upgrade (replace itself)](#upgrade-replace-itself)
    * [Uninstall](#uninstall)
    * [Dependency](#dependency)
* [Supported mode](#supported-mode)
    * [Qemu-system cooperation](#qemu-system-cooperation)
    * [Qemu-user cooperation](#qemu-user-cooperation)
    * [Intel Pin/SDE cooperation](#intel-pinsde-cooperation)
    * [KGDB cooperation](#kgdb-cooperation)
    * [Qiling framework cooperation](#qiling-framework-cooperation)
* [Added / Improved features](#added--improved-features)
    * [Qemu-system cooperation - General](#qemu-system-cooperation---general)
    * [Qemu-system cooperation - Linux specific](#qemu-system-cooperation---linux-specific)
    * [Qemu-system cooperation - Arch specific](#qemu-system-cooperation---arch-specific)
    * [Qemu-user cooperation - General](#qemu-user-cooperation---general)
    * [Heap dump features](#heap-dump-features)
    * [Improved features](#improved-features)
    * [New features](#new-features)
    * [Other](#other)
* [Memo (Japanese)](#memo-japanese)

## What is this?
This is a fork of [GEF](https://github.com/hugsy/gef).
However, it is specialized for x86 / x64 / ARM / ARM64, and various features are added.

## Setup

### Install

```bash
# Run with root user (sudo is NOT recommended)
wget -q https://raw.githubusercontent.com/bata24/gef/dev/install.sh -O- | sh
```

GEF is installed under `/root` to simplify the installation script.
If you want to change the location, please modify accordingly.

### Install (Ubuntu 23.04)

```bash
# Ubuntu 23.04 restricts global installation with pip3, so you need --break-system-packages option.
wget -q https://raw.githubusercontent.com/bata24/gef/dev/install.sh -O- | sed -e 's/\(pip3 install\)/\1 --break-system-packages/g' | sh
```

### Upgrade (replace itself)
```bash
python3 /root/.gdbinit-gef.py --upgrade
```

### Uninstall

```bash
rm -f /root/.gdbinit-gef.py /root/.gef.rc
sed -i -e '/source \/root\/.gdbinit-gef.py/d' /root/.gdbinit
```

### Dependency
See [install.sh](https://github.com/bata24/gef/blob/dev/install.sh) or
[install-minimal.sh](https://github.com/bata24/gef/blob/dev/install-minimal.sh).

## Supported mode

* Normal debugging (start under gdb)
* Attach to the process
* Attach to the process in another pid namespace
* Connect to gdbserver
* Connect to the gdb stub of qemu-system (via localhost:1234)
* Connect to the gdb stub of qemu-user (via localhost:1234)
* Connect to the gdb stub of Intel Pin (via localhost:1234)
* Connect to the gdb stub of Intel SDE (via localhost:1234)
* Connect to the gdb stub of KGDB (over serial. currently, only gdb 12.x~ is supported)
* Connect to the gdb stub of qiling framework (via localhost:9999)

### Qemu-system cooperation
* It works with any version qemu-system, but qemu-6.x or higher is recommended.
    * Start qemu-system with the `-s` option and listen on `localhost:1234`.
    * Attach with `gdb-multiarch -ex 'target remote localhost:1234'`.
    * Or `gdb-multiarch -ex 'set architecture TARGET_ARCH' -ex 'target remote localhost:1234'`.
    * Most commands should work fine unless `CONFIG_RANDSTRUCT` is enabled.
* Supported architectures
    * x86, x64, ARM and ARM64

### Qemu-user cooperation
* It works with any version qemu-user, but qemu-6.x or higher is recommended.
    * Start qemu-user with the `-g 1234` option and listen on `localhost:1234`.
    * Attach with `gdb-multiarch /PATH/TO/BINARY -ex 'target remote localhost:1234'`.
    * Or `gdb-multiarch -ex 'set architecture TARGET_ARCH' -ex 'target remote localhost:1234'`.
* Supported architectures
    * See [QEMU-USER-SUPPORTED-ARCH.md](https://github.com/bata24/gef/blob/dev/QEMU-USER-SUPPORTED-ARCH.md)

### Intel Pin/SDE cooperation
* Intel Pin:
    * Listen with `pin -appdebug -appdebug_server_port 1234 -t obj-intel64/inscount0.so -- /bin/ls`.
    * Attach with `gdb-multiarch /PATH/TO/BINARY -ex 'target remote localhost:1234'`.
    * It runs very slowly and is not recommended.
* Intel SDE:
    * Listen with `sde64 -debug -debug-port 1234 -- /bin/ls`.
    * Attach with `gdb-multiarch /PATH/TO/BINARY -ex 'target remote localhost:1234'`.
    * It runs very slowly and is not recommended.

### KGDB cooperation
* It works only gdb 12.x~.
    * Build your kernel as `CONFIG_KGDB=y`. Ubuntu has supported it by default.
    * Configure the serial port as a named pipe in your two (debugger/debuggee) virtual machine settings, such as VMware or VirtualBox.
    * Debuggee: Edit `/etc/default/grub` and append `kgdboc=ttyS0,115200 kgdbwait` to the end of `GRUB_CMDLINE_LINUX_DEFAULT`, then `update-grub && reboot`.
    * Debugger: `gdb-multiarch -ex 'target remote /dev/ttyS0'`.
    * It runs very slowly and is not recommended.
    * Commands for Qemu-system are not supported in KGDB mode (Because there is no way to access physical memory).

### Qiling framework cooperation
* This is an experimental support.
    * Write a harness. See https://docs.qiling.io/en/latest/debugger/
    * `gdb-multiarch /PATH/TO/BINARY -ex 'target remote localhost:9999'`
    * On ARM64, the flag register is not available, so the branch taken/not detected is incorrect.

## Added / Improved features

All of these features are experimental.
Tested on Ubuntu 22.04. It may work under Ubuntu 20.04 and 23.04.

### Qemu-system cooperation - General
* `qreg`: displays the register values from qemu-monitor (allows to get like `$cs` even under qemu 2.x).
    * It is shortcut for `monitor info registers`.
    * It also prints the details of the each bit of the system register when x64/x86.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/qreg.png)
* `sysreg`: pretty prints system registers.
    * It is the result of `info registers` with filtering general registers.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/sysreg.png)
* `pagewalk`: displays the page table from scanning physical memory.
    * x64 (Supported: PML5T/PML4T)
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/pagewalk-x64.png)
    * x86 (Supported: PAE/Non-PAE)
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/pagewalk-x86.png)
    * ARM64 (Supported: EL1&0-stage1/EL1&0-stage2/EL2&0-stage1/EL2-stage1/EL3-stage1)
        * ARM v8.7 base.
        * 32bit mode is NOT supported.
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/pagewalk-arm64.png)
        * Supported stage2 translation. This is EL1/EL2/EL3 pagewalk sample (HITCON CTF 2018 super_hexagon).
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/pagewalk-arm64-el123.png)
        * Secure memory scanning is supported, but you have to break in the secure world.
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/pagewalk-arm64-secure.png)
        * Pseudo page tables without detailed flags and permission can be output even in the normal world.
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/pagewalk-arm64-secure-pseudo.png)
    * ARM (only Cortex-A, LPAE/Non-LPAE, PL0/PL1)
        * ARM v7 base.
        * PL2 is NOT supported.
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/pagewalk-arm.png)
        * Secure memory scanning is supported, you don't have to break in the secure world (use register with `_S` suffix).
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/pagewalk-arm-secure.png)
* `v2p`, `p2v`: displays transformation virtual address <-> physical address.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/v2p-p2v.png)
* `xp`: is a shortcut for physical memory dump.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/xp.png)

### Qemu-system cooperation - Linux specific
* `ksymaddr-remote`: displays kallsyms information from scanning kernel memory (heuristic).
    * Supported kernel versions are not only before v6.1, but also after v6.2 (slightly changed structure in memory).
    * Supported kernel after v6.4 (changed structure in memory again).
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/ksymaddr-remote.png)
* `ksymaddr-remote-apply`: applies kallsyms information obtained by `ksymaddr-remote` to gdb.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/ksymaddr-remote-apply.png)
* `vmlinux-to-elf-apply`: applies kallsyms information obtained by `vmlinux-to-elf` to gdb.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/vmlinux-to-elf-apply1.png)
    * Once you get symboled vmlinux file, you can reuse and apply it automatically even after rebooting qemu-system.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/vmlinux-to-elf-apply2.png)
    * TIPS: `vmlinux-to-elf-apply` and `ksymaddr-remote-apply` provide almost the same functionality.
        * For normal use, I think `vmlinux-to-elf-apply` is preferable because reusing image makes it faster.
        * For FGKASLR, I think `ksymaddr-remote-apply` is preferable because faster without reusing image.
* `slub-dump`: dumps slub free-list (heuristic).
    * Supported on x64/x86/ARM64/ARM + SLUB + no-symbol + kASLR.
    * Supported on both `CONFIG_SLAB_FREELIST_HARDENED` is `y` or `n`.
    * It supports to dump partial pages (`-v`) and NUMA node pages (`-vv`).
    * Since `page_to_virt` is difficult to implement, it will heuristically determine the virtual address from the freelist.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/slub-dump.png)
* `slab-dump`: dumps slab free-list (heuristic).
    * Supported on x64 + SLAB + no-symbol + kASLR.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/slab-dump.png)
* `slob-dump`: dumps slob free-list (heuristic).
    * Supported on x64 + SLOB + no-symbol + kASLR.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/slob-dump.png)
* `slub-tiny-dump`: dumps slub-tiny free-list (heuristic).
    * Supported on x64/x86 + SLUB_TINY + no-symbol + kASLR.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/slub-tiny-dump.png)
* `kbase`: displays the kernel base address.
* `kversion`: displays the debugged kernel version.
* `kcmdline`: displays the debugged kernel startup cmdline.
* `kcurrent`: displays current task address.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/kbase-kversion-kcmdline-kcurrent.png)
* `ktask`: displays each task address.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/ktask.png)
    * It also displays the memory map of the user-land process.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/ktask-maps.png)
    * It also displays the register values saved on kstack of the user-land process.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/ktask-regs.png)
* `kmod`: displays each module address.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/kmod.png)
    * It also displays each module symbols.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/kmod-syms.png)
* `kcdev`: displays each character device information.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/kcdev.png)
* `kbdev`: displays each block device information.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/kbdev.png)
* `kops`: displays each operations member.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/kops.png)
* `syscall-table-view`: displays system call table.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/syscall-table-view.png)
    * It also dumps ia32/x32 syscall table under x64.
    * It also dumps compat syscall table under ARM64.
* `thunk-hunter`: collects and displays the thunk function addresses that are called automatically (only x64/x86).
    * If this address comes from RW area, this is useful for getting RIP.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/thunk-hunter.png)
* `usermodehelper-hunter`: collects and displays the information that is executed by `call_usermodehelper_setup`.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/usermodehelper-hunter.png)
* `kmagic`: displays useful addresses in kernel.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/kmagic.png)
* `kchecksec`: checks kernel security.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/kchecksec.png)
* `kparam-sysctl`: dumps sysctl parameters (heuristic).
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/kparam-sysctl.png)
* `kfilesystems`: dumps supported file systems.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/kfilesystems.png)
* `kclock-source`: dumps clocksource list.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/kclock-source.png)
* `ksearch-code-ptr`: searches the code pointer in kernel data area.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/ksearch-code-ptr.png)
* `kdmesg`: dumps the ring buffer of dmesg area.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/kdmesg.png)
* `pagewalk-with-hints`: prints pagetables with description.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/pagewalk-with-hints.png)
* `xslubobj`: resolves which `kmem_cache` certain address (object) belongs to (only x64).
    * If the chunk of `slub` that the address (object) belongs to is all used, it cannot be displayed with `slub-dump`.
    * Even with such an address (object), this command may be able to resolve `kmem_cache`.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/xslubobj.png)
* `kmalloc-hunter`: collects and displays information when kmalloc/kfree.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/kmalloc-hunter.png)

### Qemu-system cooperation - Arch specific
* `uefi-ovmf-info`: dumps addresses of some important structures in each boot phase of UEFI when OVMF is used (heuristic).
    * Supported on only x64.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/uefi-ovmf-info.png)
* `msr`: displays MSR (Model Specific Registers) values by embedding/executing dynamic assembly.
    * Supported on x64/x86 WITHOUT `-enable-kvm`.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/msr.png)
* `xsm`: dumps secure memory when gdb is in normal world.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/xsm.png)
* `wsm`: writes the value to secure memory when gdb is in normal world.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/wsm.png)
* `bsm`: sets the breakpoint to secure memory when gdb is in normal world.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/bsm.png)
* `optee-break-ta`: sets the breakpoint to the offset of OPTEE-Trusted-App when gdb is in normal world.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/optee-break-ta.png)

### Qemu-user cooperation - General
* `si`/`ni`: are the wrapper for native `si`/`ni`.
    * On s390x architecture, a `PC not saved` error may be output when executing `stepi`/`nexti`.
    * But the execution itself is fine, so this command ignores this error and executes `context` normally.
    * On OpenRISC architecture, branch operations don't work well, so use breakpoints to simulate.
    * On Cris architecture, `stepi`/`nexti` commands don't work well, so use breakpoints to simulate.
    * If you want to use native `si`/`ni`, use the full form `stepi`/`nexti`.
* `c`: is the wrapper for native `c`.
    * When connecting to gdb stub of qemu-user or Intel Pin, gdb does not trap SIGINT during `continue`.
    * If you want to trap, you need to issue SIGINT on the qemu-user or pin side, but switching screens is troublesome.
    * This command realizes a pseudo SIGINT trap by trapping SIGINT on the python side and throwing SIGINT back to qemu-user or Intel Pin.
    * It works only local qemu-user or Intel Pin.
    * If you want to use native `c`, use the full form `continue`.

### Heap dump features
* `partition-alloc-dump`: dumps partition-alloc free-list (heuristic).
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/partition-alloc-dump.png)
    * This command is reserved for the implementation of latest version of chromium.
        * Currently tested: v116.x / 1154341 / 8a942c7ef88b81643f77827fd3a16154bba4a600
        * https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=Linux_x64/1154341/
    * Supported on only x64 (maybe it works on x86/ARM/ARM64, but not tested).
    * It will try heuristic search if binary has no symbol.
    * How to test:
        * See [partition-alloc-dump-dev/downloader.py](https://github.com/bata24/gef/blob/dev/partition-alloc-dump-dev/downloader.py).
* `tcmalloc-dump`: dumps tcmalloc free-list (heuristic).
    * Supported on only x64, based on gperftools-2.9.1 (named `libgoogle-perftools{4,-dev}`)
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/tcmalloc-dump.png)
    * How to test:
        * Execute as `LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtcmalloc.so ./a.out`.
* `musl-heap-dump`: dumps musl-libc heap chunks (heuristic).
    * Supported on x64/x86, based on musl-libc v1.2.4.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/musl-heap-dump.png)
    * How to test:
        * Get and extract latest source, then `./configure && make install`.
        * Build as `/usr/local/musl/bin/musl-gcc test.c`.
* `uclibc-ng-heap-dump`: dumps uClibc-ng heap chunks (heuristic).
    * Supported on x64/x86, based on uClibc-ng v1.0.42 malloc-standard.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/uclibc-ng-heap-dump.png)
    * How to test (x64):
        * Download and extract `x86-64--uclibc--stable-2022.08-1.tar.bz2` from https://toolchains.bootlin.com/
        * Add `/path/to/toolchain/bin` to `$PATH`, then `x86_64-linux-gcc test.c`.
        * Fix interpreter by `patchelf --set-interpreter /PATH/TO/x86_64-buildroot-linux-uclibc/sysroot/lib/ld64-uClibc.so.0 a.out`.
* `optee-bget-dump`: dumps bget allocator of OPTEE-Trusted-App.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/optee-bget-dump.png)

### Improved features
* `vmmap`: is improved.
    * It displays the meomry map information even when connecting to gdb stub like qemu-user (heuristic).
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/vmmap-qemu-user.png)
    * Intel Pin is supported.
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/vmmap-pin.png)
    * Intel SDE is supported.
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/vmmap-sde.png)
    * It is redirected to `pagewalk` when connecting to gdb stub of qemu-system.
* Glibc heap commands are improved.
    * It changes the color.
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/heap-bins.png)
    * They print info if the chunk is in free-list.
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/heap-if-in-freelist.png)
    * Thread arena is supported for all `heap` commands.
        * Use `-a` option.
    * `find-fake-fast`: searches for a memory with a size-like value that can be linked to the fastbin free-list.
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/find-fake-fast.png)
    * `visual-heap`: is colorized heap viewer.
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/visual-heap.png)
    * `extract-heap-addr`: analyzes tcache-protected-fd introduced from glibc-2.32.
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/extract-heap-addr.png)
* `registers`: is improved.
    * It also shows raw values of flag register, current ring, exception level, secure state, etc.
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/registers-x64.png)
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/registers-arm64.png)
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/registers-arm.png)
* `context`: is improved.
    * It supports automatic display of system call arguments when calling a system call.
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/context-syscall-args.png)
    * It supports automatic display of address and value when accessing memory.
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/context-memory-access.png)
    * It supports smart symbol printing for cpp function.
        * ex: `std::map<int, std::map<int, int>>` will be replaced by `std::map<...>`.
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/smart-cpp-function-name.png)
        * command: `gef config context.smart_cpp_function_name true` or `smart-cpp-function-name` (later is used to toggle).
* `telescope`: is improved.
    * It displays ordinal numbers as well as offsets.
    * It displays if there are canary and ret-addr on the target area.
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/telescope.png)
    * It supports blacklist address features (to avoid dying when touching the address mapped to the serial device).
    * It also shows the symbol if available.
* `proc-info`: is improved.
    * It displays some additional informations.
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/proc-info.png)
* `elf-info`: is improved.
    * It displays Program Header and Section Header.
    * It supports parsing from memory.
    * It supports parsing remote binary (if download feature is available).
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/elf-info.png)
* `checksec`: is improved.
    * It shows whether Static or Dynamic.
    * It shows whether Stripped or not.
    * It detects canary against static stripped binary.
    * It shows whether Intel CET instructions (`endbr64`/`endbr32`) is found or not.
    * It shows whether Intel CET IBT/SHSTK is enabled or not.
    * It shows whether ARMv8 PAC / MTE is enabled or not.
    * It shows whether RPATH/RUNPATH is set or not.
    * It shows if Clang CFI/SafeStack is used or not.
    * It shows whether System-ASLR is enabled or not.
    * It shows whether GDB ASLR setting is enabled or not.
    * It supports parsing remote binary (if download feature is available).
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/checksec.png)
* `got`: is improved.
    * It displays not only GOT address but also PLT address.
    * It scans `.plt.sec` section if Intel CET is enabled.
    * It can also display the GOT of the library.
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/got.png)
    * It can also display `type`, `offset`, `reloc_arg`, `section` and `permission`.
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/got-v.png)
* `canary`: is improved.
    * It displays all canary positions in memory.
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/canary.png)
* `edit-flags`: is improved.
    * It displays the meaning of each bit if `-v` option is provided.
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/edit-flags-x64.png)
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/edit-flags-arm.png)
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/edit-flags-arm64.png)
* `unicorn-emulate`: is improved.
    * It reads and writes correctly to the address pointed to by `$fs`/`$gs`.
    * It supports a new mode to stop after executing N instructions (`-g`).
    * It shows changed memories.
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/unicorn-emulate.png)
* `ropper`: is improved.
    * It does not reset autocomplete settings after calling imported ropper.
* `hexdump`: is improved.
    * It supports physical memory if under qemu-system.
    * It will retry with adjusting read size when failed reading memory.
    * By default, the same line is omitted.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/hexdump.png)
* `patch`: is improved.
    * It supports physical memory if under qemu-system.
    * Added some new modes: `pattern`, `hexstring`, `history`, `revert`, `nop`, `inf`, `trap`, `ret`, and `syscall`.
    * `nop` command has been integrated into `patch` command.
* `search-pattern`: is improved.
    * It supports when under qemu-system (in short, it works without `/proc/self/maps`)
    * It supports aligned search.
    * It supports hex string specification.
    * It also searches UTF-16 string if target string is ASCII.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/search-pattern.png)

### New features
* `pid`: prints pid.
* `filename`: prints filename.
* `auxv`: pretty prints ELF auxiliary vector.
    * Supported also under qemu-user (heuristic).
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/auxv.png)
* `argv`/`envp`: pretty prints argv and envp.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/argv-envp.png)
* `gdtinfo`: pretty prints GDT sample.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/gdtinfo.png)
* `idtinfo`: pretty prints IDT sample.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/idtinfo.png)
* `tls`: pretty prints TLS area.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/tls.png)
* `fsbase`,`gsbase`: pretty prints `$fs_base`, `$gs_base`.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/fsbase_gsbase.png)
* `libc`/`ld`/`heapbase`/`codebase`: displays each of the base address.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/base.png)
* `brva`: sets a breakpoint at relative offset from codebase.
* `fpu`/`mmx`/`sse`/`avx`: pretty prints FPU/MMX/SSE/AVX registers.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/fpu-mmx-sse-avx.png)
* `xmmset`: sets the value to xmm/ymm register simply.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/xmmset.png)
* `mmxset`: sets the value to mm register simply.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/mmxset.png)
* `exec-until`: executes until specified operation.
    * Supported following patterns of detection.
        * call
        * jmp
        * syscall
        * ret
        * indirect-branch (only x86/x64)
        * all-branch (call || jmp || ret)
        * memory-access (detect just `[...]`)
        * specified-keyword-regex
        * specified-condition (expressions using register or memory values)
        * user-code
        * libc-code
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/exec-until.png)
* `until-next`: executes until next address.
    * This is useful for the operation with `rep` prefix.
* `add-symbol-temporary`: adds symbol information from command-line.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/add-symbol-temporary.png)
* `errno`: displays errno list or specified errno.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/errno.png)
* `u2d`: shows cast/transformation u64 <-> double/float.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/u2d.png)
* `trans`: shows various transformation.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/trans.png)
* `hash-memory`: calculates various hashes/CRCs.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/hash-memory.png)
* `memcmp`: compares the contents of the address A and B, whether virtual or physical.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/memcmp.png)
* `memcpy`: copies the contents from the address A to B, whether virtual or physical.
* `memswap`: swaps the contents of the address A and B, whether virtual or physical.
* `meminsert`: inserts the contents of the address A to B, whether virtual or physical.
* `is-mem-zero`: checks the contents of address range is all 0x00 or 0xff or not.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/is-mem-zero.png)
* `ii`: is a shortcut for `x/50i $pc` with opcode bytes.
    * It prints the value if it is memory access operation.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/ii.png)
* `version`: shows software versions that gef used.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/version.png)
* `follow`: changes `follow-fork-mode` setting.
* `smart-cpp-function-name`: toggles `context.smart_cpp_function_name` setting.
* `seccomp`: invokes `seccomp-tools`.
* `onegadget`: invokes `one_gadget`.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/onegadget.png)
* `ls`/`cat`: invokes `ls`/`cat` directly.
* `smart-memory-dump`: dumps all regions of the memory to each file.
* `mmap`: allocates a new memory if `mmap` symbol exists.
    * This is syntax sugar of `call mmap(...)`.
* `constgrep`: invokes `grep` under `/usr/include`.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/constgrep.png)
* `time`: measures the time of the GDB command.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/time.png)
* `multi-line`: executes multiple GDB commands in sequence.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/multi-line.png)
* `rp`: invokes `rp++` with commonly used options.
* `cpuid`: shows the result of cpuid(eax=0,1,2...).
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/cpuid.png)
* `dasm`: disassembles the code by capstone.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/dasm.png)
* `asm-list`: lists up instructions. (only x86/x64)
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/asm-list.png)
    * This command uses x86data.js from https://github.com/asmjit/asmdb
* `syscall-search`: searches system call by regex.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/syscall-search.png)
* `dwarf-exception-handler`: dumps the DWARF exception handler informations.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/dwarf-exception-handler.png)
* `magic`: displays useful addresses in glibc etc.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/magic.png)
* `dynamic`: dumps the `_DYNAMIC` area.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/dynamic.png)
* `link-map`: dumps useful members of `link_map` with iterating.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/link-map.png)
* `ret2dl-hint`: shows the structure used by Return-to-dl-resolve as hint.
* `srop-hint`: shows the code for SigReturn-Oriented-Programming as hint.
* `dtor-dump`: dumps some destructor functions list.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/dtor-dump.png)
* `walk-link-list`: walks the link list.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/walk-link-list.png)
* `ptr-mangle`: shows the mangled value will be mangled by `PTR_MANGLE`.
* `ptr-demangle`: shows the demangled value of the value mangled by `PTR_MANGLE`.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/ptr-mangle-demangle.png)
* `search-mangled-ptr`: searches the mangled value from RW memory.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/search-mangled-ptr.png)
* `capability`: shows the capabilities of the debugging process.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/capability.png)
* `arch-info`: shows architecture information used in gef.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/arch-info.png)
* `call-syscall`: calls system call with specified values.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/call-syscall.png)
* `ascii-search`: searches ASCII string recursively from specific location.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/ascii-search.png)
* `read-system-register`: reads system register for old qemu.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/read-system-register.png)
* `pac-keys`: pretty prints ARM64 PAC keys.
* `message-break`: sets a breakpoint with simple user defined message as f-string format.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/message-break.png)
* `hexdump-flexible`: displays the hexdump with user defined format.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/hexdump-flexible.png)
* `v8`: displays v8 tagged object.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/v8.png)
    * It also loads more commands from latest gdbinit for v8.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/v8-load.png)
* `main-break`: sets a breakpoint at `main` with or without symbols, then continue.
    * Useful if you just want to run to `main` when using qemu-user or pin.
* `distance`: calculates the offset from its base address.

### Other
* The category is introduced in `gef help`.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/gef-help.png)
* Combined into one file (from gef-extra). The followings are moved from gef-extras.
    * `peek-pointers`, `current-stack-frame`, `xref-telescope`, `bytearray`, and `bincompare`.
    * This is because a single file is more attractive than ease of maintenance.
* The system-call table used by `syscall-args` is moved from gef-extras.
    * It was updated up to linux kernel 6.3.9 for each architecture.
* Removed some features I don't use.
    * `$`, `ida-interact`, `gef-remote`, `pie`, `pcustom`, `ksymaddr`, `trace-run`, `bufferize`, `output redirect` and `shellcode`.
* Many bugs fix / formatting / made it easy for me to use.

## Memo (Japanese)
* Why I decided to make this
    * [gefを改造した話](https://hackmd.io/@bata24/rJVtBJsrP)
* The story behind each command, etc.
    * [bata24/gefの機能紹介とか](https://hackmd.io/@bata24/SycIO4qPi)
