## Image
![](https://raw.githubusercontent.com/bata24/gef/dev/images/context.png)

## Table of Contents
* [What is this?](#what-is-this)
* [Setup](#setup)
    * [Supported environment](#supported-environment)
    * [Install](#install)
    * [Upgrade](#upgrade)
    * [Uninstall](#uninstall)
    * [Dependency](#dependency)
* [Added / improved features](#added--improved-features)
    * [Supported mode](#supported-mode)
    * [Qemu-system cooperation](#qemu-system-cooperation)
    * [Qemu-user cooperation](#qemu-user-cooperation)
    * [Heap dump features](#heap-dump-features)
    * [Improved features](#improved-features)
    * [Added features](#added-features)
    * [Other](#other)
* [FAQ](#faq)

## What is this?
This is a fork of [GEF](https://github.com/hugsy/gef) with 3 major improvements.

1. Added many heuristic commands for kernel debugging __WITHOUT a symbolized vmlinux__ (for qemu-system; linux kernel 3.x ~ 6.13.x).
2. Added support for [many architectures](https://github.com/bata24/gef/blob/dev/docs/QEMU-USER-SUPPORTED-ARCH.md) (for qemu-user).
3. Added some heap dump commands for various allocators.

Many other commands have been added and improved. Enjoy!

## Setup

### Supported environment
- Tested on Ubuntu 24.04.
- It may work on Ubuntu 22.04 - 23.10.
- It might work on Ubuntu 20.04 - 21.10, but it is not recommended.

### Install
* Run following commands as root user.
    ```bash
    # Ubuntu 23.04 or later restrict global installation of python packages with pip3.
    # So you need --break-system-packages option.
    wget -q https://raw.githubusercontent.com/bata24/gef/dev/install.sh -O- | sed -e 's/pip3 install/pip3 install --break-system-packages/g' | sh

    # Ubuntu 22.10 or before
    wget -q https://raw.githubusercontent.com/bata24/gef/dev/install.sh -O- | sh
    ```
* Note
    * To simplify the installation script, GEF (`gef.py`) is installed to a fixed path (`/root/.gdbinit-gef.py`).
    * Also, it registers the GEF path to `/root/.gdbinit`.
    * If you want to change the location or user, please modify both yourself.
    * See [docs/FAQ.md](https://github.com/bata24/gef/blob/dev/docs/FAQ.md) for more information and other install options.
        * There is a way to install it using `venv`.
        * There is a minimum installation that reduces installation as much as possible.

### Upgrade
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

## Added / improved features

### Supported mode
* Normal debugging
* Attach to the process
* Attach to the process in another namespace (e.g., attaching from outside of `docker`)
* Connect to `gdbserver`
* Connect to the gdb stub of `qemu-system`
* Connect to the gdb stub of `qemu-user`
* Connect to the gdb stub of `Intel Pin`
* Connect to the gdb stub of `Intel SDE`
* Connect to the gdb stub of `qiling framework`
* Connect to the gdb stub of `KGDB` (need gdb 12~)
* Connect to the gdb stub of `VMWare`
* Connect to the gdb stub of `wine`
* Record and replay debugging (`rr replay`)

See [docs/SUPPORTED-MODE.md](https://github.com/bata24/gef/blob/dev/docs/SUPPORTED-MODE.md) for detail.

### Qemu-system cooperation
* `pagewalk`: scans physical memory, parses page tables, and displays memory maps.
    * x64 (Supported: 4-Level/5-Level Paging)
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/pagewalk-x64.png)
    * x86 (Supported: PAE/Non-PAE)
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/pagewalk-x86.png)
    * ARM64 (Supported: only Cortex-A, EL0-EL3, stage1-2)
        * ARM v8.7 base. 32bit mode is NOT supported.
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/pagewalk-arm64.png)
        * Here is a sample of each level pagewalk from HITCON CTF 2018 `super_hexagon`.
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/pagewalk-arm64-el123.png)
        * Secure memory scanning is also supported, but you have to break in the secure world.
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/pagewalk-arm64-secure.png)
        * Pseudo memory map without detailed flags and permission can be output even in the normal world (when OP-TEE).
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/pagewalk-arm64-secure-pseudo.png)
    * ARM (Supported: only Cortex-A, LPAE/Non-LPAE, PL0/PL1)
        * ARM v7 base. PL2 is NOT supported.
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/pagewalk-arm.png)
        * Secure memory scanning is also supported, and you don't have to break in the secure world (unlike ARM64).
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/pagewalk-arm-secure.png)
* `pagewalk-with-hints`: prints pagetables with description.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/pagewalk-with-hints.png)
* `v2p`/`p2v`: displays transformation virtual address <-> physical address.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/v2p-p2v.png)
* `xp`: is a shortcut for physical memory dump.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/xp.png)
* `qreg`: displays the register values from qemu-monitor (allows to get like `$cs` even under qemu 2.x).
    * It is a shortcut for `monitor info registers`.
    * It also prints the details of the each bit of the system register when x64/x86.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/qreg.png)
* `sysreg`: pretty prints system registers.
    * It shows `info registers` results, excluding general registers.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/sysreg.png)
* `msr`: reads/writes MSR (Model Specific Registers) value by embedding/executing dynamic assembly.
    * Supported on x64 and x86.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/msr.png)
* `kbase`: displays the kernel base address.
* `kversion`: displays the kernel version.
* `kcmdline`: displays the kernel cmdline used at boot time.
* `kcurrent`: displays current task address.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/kbase-kversion-kcmdline-kcurrent.png)
* `ksymaddr-remote`: displays kallsyms information from scanning kernel memory.
    * Supported kernel versions: 3.x to 6.13.x.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/ksymaddr-remote.png)
* `ksymaddr-remote-apply`/`vmlinux-to-elf-apply`: applies kallsyms information obtained by `ksymaddr-remote` or `vmlinux-to-elf` to gdb.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/ksymaddr-remote-apply.png)
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/vmlinux-to-elf-apply.png)
    * Once you get symboled pseudo ELF file, you can reuse and apply it automatically even after rebooting qemu-system.
    * `vmlinux-to-elf-apply` and `ksymaddr-remote-apply` provide almost the same functionality.
        * `vmlinux-to-elf-apply`: Requires installation of external tools. Create `vmlinux` with symbols.
        * `ksymaddr-remote-apply`: Requires no external tools. Create an blank ELF with only embedded symbols.
* `slub-dump`: dumps slub free-list.
    * Supported on x64/x86/ARM64/ARM + `SLUB` + no-symbol + kASLR.
    * Supported on both `CONFIG_SLAB_FREELIST_HARDENED` is `y` or `n`.
    * It supports to dump partial pages (`-v`) and NUMA node pages (`-vv`).
    * Since `page_to_virt` is difficult to implement, it will heuristically determine the virtual address from the free-list.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/slub-dump.png)
* `slab-dump`: dumps slab free-list.
    * Supported on x64/x86/ARM64/ARM + `SLAB` + no-symbol + kASLR.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/slab-dump.png)
* `slob-dump`: dumps slob free-list.
    * Supported on x64/x86/ARM64/ARM + `SLOB` + no-symbol + kASLR.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/slob-dump.png)
* `slub-tiny-dump`: dumps slub-tiny free-list.
    * Supported on x64/x86/ARM64/ARM + `SLUB-TINY` + no-symbol + kASLR.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/slub-tiny-dump.png)
* `slab-contains`: resolves which `kmem_cache` certain address (object) belongs to (for `SLUB`/`SLUB-TINY`/`SLAB`).
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/slab-contains.png)
    * For `SLUB`/`SLUB-TINY`, if all chunks belonging to a certain `page` are in use, they will not be displayed by `slub-dump`/`slub-tiny-dump` command.
    * Even with such an address (object), this command may be able to resolve `kmem_cache`.
* `buddy-dump`: dumps zone of page allocator (buddy allocator) free-list.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/buddy-dump.png)
* `vmalloc-dump`: dumps `vmalloc` used-list and freed-list.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/vmalloc-dump.png)
* `page`: displays transformation `struct page` <-> virtual/physical address.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/page.png)
    * There are shortcuts: `virt2page`, `page2virt`, `phys2page` and `page2phys`.
* `kchecksec`: checks kernel security.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/kchecksec.png)
* `kmagic`: displays useful addresses in kernel.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/kmagic.png)
* `kconfig`: dumps kernel config if available.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/kconfig.png)
* `syscall-table-view`: displays system call table.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/syscall-table-view.png)
    * It also dumps ia32/x32 syscall table under x64.
    * It also dumps compat syscall table under ARM64.
* `ksysctl`: dumps sysctl parameters.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/ksysctl.png)
* `ktask`: displays each task address.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/ktask.png)
    * It also displays the memory map of the userland process.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/ktask-maps.png)
    * It also displays the register values saved on kstack of the userland process.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/ktask-regs.png)
    * It also displays the file descriptors of the userland process.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/ktask-fd.png)
    * It also displays the signal handlers of the userland process.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/ktask-sighands.png)
    * It also displays the namespaces of the userland process.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/ktask-namespaces.png)
    * It also displays the seccomp-filter.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/ktask-seccomp.png)
* `kmod`: displays each module address.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/kmod.png)
    * It also displays each module symbols.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/kmod-syms.png)
* `kload`: loads vmlinux without loaded address.
    * It is useful if you have a vmlinux with debuginfo at hand.
* `kmod-load`: loads the kernel module without loaded address.
    * It is useful if you have a kernel module with debuginfo at hand.
* `kops`: displays each operations member.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/kops.png)
* `kcdev`: displays each character device information.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/kcdev.png)
* `kbdev`: displays each block device information.
    * If there are too many block devices, detection will not be successful.
    * This is because block devices are not managed in one place, so I use the list of `bdev_cache` obtained from the slub-dump results.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/kbdev.png)
* `kfilesystems`: dumps supported file systems.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/kfilesystems.png)
* `kclock-source`: dumps clocksource list.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/kclock-source.png)
* `kdmesg`: dumps the ring buffer of dmesg area.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/kdmesg.png)
* `kpipe`: displays each pipe information.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/kpipe.png)
* `kbpf`: dumps bpf information.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/kbpf.png)
* `ktimer`: dumps timer.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/ktimer.png)
* `kpcidev`: dumps PCI devices.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/kpcidev.png)
* `kipcs`: dumps IPCs information (System V semaphore, message queue and shared memory).
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/kipcs.png)
* `kdevio`: dumps I/O-port and I/O-memory information.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/kdevio.png)
* `kdmabuf`: dumps DMA-BUF information.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/kdmabuf.png)
* `kirq`: dumps irq information.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/kirq.png)
* `knetdev`: displays net devices.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/knetdev.png)
* `ksearch-code-ptr`: searches the code pointer in kernel data area.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/ksearch-code-ptr.png)
* `thunk-tracer`: collects and displays the thunk function addresses that are called automatically (only x64/x86).
    * If this address comes from RW area, this is useful for getting RIP.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/thunk-tracer.png)
* `usermodehelper-tracer`: collects and displays the information that is executed by `call_usermodehelper_setup`.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/usermodehelper-tracer.png)
* `kmalloc-tracer`: collects and displays information when `kmalloc`/`kfree`.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/kmalloc-tracer.png)
* `kmalloc-allocated-by`: calls a predefined set of system calls and prints structures allocated by `kmalloc` or freed by `kfree`.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/kmalloc-allocated-by.png)
* `ktrace`: traces kernel functions and arguments.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/ktrace.png)
* `xsm`: dumps secure memory when gdb is in normal world.
    * Supported on ARM64 and ARM.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/xsm.png)
* `wsm`: writes the value to secure memory when gdb is in normal world.
    * Supported on ARM64 and ARM.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/wsm.png)
* `bsm`: sets the breakpoint to secure memory when gdb is in normal world.
    * Supported on ARM64 and ARM.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/bsm.png)
* `optee-break-ta`: sets the breakpoint to the offset of OPTEE-Trusted-App when gdb is in normal world.
    * Supported on ARM64 and ARM.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/optee-break-ta.png)
* `pac-keys`: pretty prints ARM64 PAC keys.
    * Supported on ARM64.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/pac-keys.png)
* `uefi-ovmf-info`: dumps addresses of some important structures in each boot phase of UEFI when OVMF is used.
    * Supported on x64.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/uefi-ovmf-info.png)
* `qemu-device-info`: dumps device information for qemu-escape (WIP).

### Qemu-user cooperation
* `si`/`ni`: are the wrapper for native `si`/`ni` if OpenRISC 1000 or CRIS.
    * On OpenRISC 1000 architecture, branch operations don't work well, so GEF uses breakpoints to simulate.
    * On CRIS architecture, `stepi`/`nexti` commands don't work well, so GEF uses breakpoints to simulate.
    * If you want to use native `si`/`ni`, use the full form `stepi`/`nexti`.
* `c`: is the wrapper for native `c` if gdb is connected to qemu-user or Intel Pin.
    * When connecting to gdb stub of qemu-user or Intel Pin, gdb does not trap `SIGINT` during `continue`.
    * If you want to trap, you need to issue `SIGTRAP` on the qemu-user or pin side, but switching screens is troublesome.
    * This command realizes a pseudo `SIGTRAP` trap by trapping `SIGINT` on the python side and throwing `SIGTRAP` back to qemu-user or Intel Pin.
    * It works only local qemu-user or Intel Pin.
    * If you want to use native `c`, use the full form `continue`.

### Heap dump features
* Glibc heap commands are improved.
    * It changes the color and print symbol if exists.
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/heap-bins.png)
    * They print bins information if the chunk is in free-list.
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/heap-if-in-freelist.png)
    * Thread arena is supported for all `heap` commands.
        * Use `-a` option.
    * It supports some new sub-commands.
        * `heap arenas`
            * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/heap-arenas.png)
        * `heap top`
            * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/heap-top.png)
        * `heap bins-simple`
            * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/heap-bins-simple.png)
        * `heap try-free`
            * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/heap-try-free.png)
        * `heap try-malloc`
            * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/heap-try-malloc.png)
        * `heap tcache-index-helper`
            * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/heap-index-helper.png)
        * `heap find-fake-fast`: searches for a memory with a size-like value that can be linked to the fastbin free-list.
            * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/heap-find-fake-fast.png)
        * `heap extract-heap-addr`: analyzes tcache-protected-fd introduced from glibc-2.32.
            * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/heap-extract-heap-addr.png)
        * `heap calc-protected-fd`: calculates a valid value as protected fd.
            * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/heap-calc-protected-fd.png)
        * `heap visual-heap`: is colorized heap viewer.
            * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/heap-visual-heap.png)
        * `heap tracer`: has been integrated from `heap-analysis-helper`.
* uClibc heap commands are added.
    * `uclibc-ng-heap-dump`: dumps uClibc-ng heap chunks.
        * Supported on x64 and x86, based on uClibc-ng v1.0.42 malloc-standard.
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/uclibc-ng-heap-dump.png)
        * How to test (x64):
            * Download and extract `x86-64--uclibc--stable-2024.05-1.tar.bz2` from https://toolchains.bootlin.com/
            * Add `/PATH/TO/x86_64-buildroot-linux-uclibc/bin` to `$PATH`, then build as `x86_64-linux-gcc test.c`.
            * Fix interpreter by `patchelf --set-interpreter /PATH/TO/x86_64-buildroot-linux-uclibc/sysroot/lib/ld64-uClibc.so.0 a.out`.
    * `uclibc-ng-visual-heap`: is colorized heap viewer for uClibc-ng.
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/uclibc-ng-visual-heap.png)
* `partition-alloc-dump`: dumps partition-alloc free-list for chromium.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/partition-alloc-dump.png)
    * This command is reserved for the implementation of latest version of chromium.
        * Currently tested: v136.x / [1428670](https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=Linux_x64/1428670/) / 22d328236f7050eb00e12030253f90e812c4e0d2
    * Supported on x64 and ARM64 (maybe it works on x86/ARM too, but not tested).
    * It will try heuristic search if binary has no symbol.
    * How to test:
        * See [dev/partition-alloc-dump/downloader.py](https://github.com/bata24/gef/blob/dev/dev/partition-alloc-dump/downloader.py).
* `tcmalloc-dump`: dumps tcmalloc (`gperftools-2.9.1` or named `libgoogle-perftools{4,-dev}`) free-list (only x64).
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/tcmalloc-dump.png)
    * How to test:
        * Execute as `LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtcmalloc.so ./a.out`.
* `musl-heap-dump`: dumps musl-libc v1.2.5 heap chunks (only x64/x86).
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/musl-heap-dump.png)
    * How to test:
        * Get and extract the latest source from https://musl.libc.org/
        * Build with `./configure && make install`.
        * Build as `/usr/local/musl/bin/musl-gcc test.c`.
* `go-heap-dump`: dumps go language v1.22.2 mheap (only x64).
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/go-heap-dump.png)
* `tlsf-heap-dump`: dumps TLSF (Two-Level Segregated Fit) v2.4.6 free-list (only x64).
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/tlsf-heap-dump.png)
    * How to test (x64):
        * Get and extract the latest source from http://www.gii.upv.es/tlsf/
        * Build with `cd TLSF-2.4.6/src && make && cd ../examples && make` then use `test1` etc.
* `hoard-heap-dump`: dumps Hoard v3.13 free-list (only x64).
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/hoard-heap-dump.png)
    * How to test (x64):
        * Get and extract the latest source from https://github.com/emeryberger/Hoard
        * Build with `cd Hoard/src && make`.
        * Execute as `LD_PRELOAD=/path/to/libhoard.so ./a.out`.
* `mimalloc-heap-dump`: dumps mimalloc free-list (only x64).
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/mimalloc-heap-dump.png)
    * How to test (x64):
        * Get and extract the latest source from https://github.com/microsoft/mimalloc
        * Build with `mkdir build && cd build && cmake .. && make`.
        * Execute as `LD_PRELOAD=/path/to/libmimalloc.so ./a.out`.
* `optee-bget-dump`: dumps bget allocator of OPTEE-Trusted-App.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/optee-bget-dump.png)

### Improved features
* `vmmap`: is improved.
    * It displays the memory map information even when connecting to gdb stub like qemu-user.
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/vmmap-qemu-user.png)
    * Intel Pin is supported.
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/vmmap-pin.png)
    * Intel SDE is supported.
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/vmmap-sde.png)
    * It is redirected to `pagewalk` when connecting to gdb stub of qemu-system.
    * It supports detection and coloring of `Writable`, `ReadOnly`, `None` and `RWX` regions.
    * It shows the area each register points to.
* `registers`: is improved.
    * It also shows raw values of flag register, current ring, exception level, secure state, etc.
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/registers-x64.png)
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/registers-arm64.png)
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/registers-arm.png)
* `context`: is improved.
    * It supports automatic display of system call arguments when calling a system call.
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/context-syscall-args.png)
    * It supports new modes:
        * `context on`
        * `context off`
    * It supports automatic display of address and value when accessing memory.
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/context-memory-access.png)
    * It supports smart symbol printing for C++ function.
        * ex: `std::map<int, std::map<int, int>>` will be replaced by `std::map<...>`.
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/smart-cpp-function-name.png)
        * command: `gef config context.smart_cpp_function_name true` or `smart-cpp-function-name` (later is used to toggle).
* `telescope`: is improved.
    * It displays ordinal numbers as well as offsets.
    * It displays if there are canary and return address on the target area.
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/telescope.png)
    * It supports blacklist address features (to avoid dying when touching the address mapped to the serial device).
    * It also shows the symbol if available.
    * It supports some new options:
        * `--is-addr`
        * `--is-not-addr`
        * `--zero`
        * `--non-zero`
        * `--tag`
        * `--uniq`
        * `--depth`
        * `--phys`
        * `--list-head`
        * `--slab-contains`
        * `--slab-contains-unaligned`
* `proc-info`: is improved.
    * It displays some additional information.
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/proc-info.png)
* `elf-info`: is improved.
    * It displays Program Header and Section Header.
    * It supports parsing from memory.
    * It supports parsing remote binary (if download feature is available).
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/elf-info.png)
* `xinfo`: is improved.
    * It shows more information.
    * It also supports kernel debugging.
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/xinfo.png)
* `checksec`: is improved.
    * It shows additional information.
        * Static or Dynamic or Static-PIE
        * Stripped or not
        * Debuginfo or not
        * Intel CET IBT/SHSTK
        * ARMv8 PAC, ARMv8 MTE
        * RPATH, RUNPATH
        * Clang CFI/SafeStack
        * System-ASLR, GDB ASLR setting
    * It supports parsing remote binary (if download feature is available).
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/checksec.png)
* `got`: is improved.
    * It displays not only GOT address but also PLT address.
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/got.png)
    * It scans `.plt.sec` section if Intel CET is enabled.
    * It can also display the GOT of the library.
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/got-libc.png)
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
    * It does not reset autocomplete settings after calling imported `ropper`.
* `hexdump`: is improved.
    * It supports physical memory if under qemu-system.
    * It will retry with adjusting read size when failed reading memory.
    * By default, the same line is omitted.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/hexdump.png)
* `patch`: is improved.
    * It supports physical memory if under qemu-system.
    * Added some new modes:
        * `patch hex`
        * `patch pattern`
        * `patch nop`
        * `patch inf`
        * `patch trap`
        * `patch ret`
        * `patch syscall`
        * `patch history`
        * `patch revert`
    * `nop` command has been integrated into `patch` command.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/patch.png)
* `search-pattern`: is improved.
    * It supports when under qemu-system (in short, it works without `/proc/self/maps`)
    * It supports some new options:
        * `--hex`
        * `--hex-regex`
        * `--aligned`
        * `--perm`
        * `--interval`
        * `--limit`
        * `--max-region-size`
        * `--phys`
    * It also searches UTF-16 string if target string is ASCII.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/search-pattern.png)
* `mprotect`: is improved.
    * Rewritten to use `call-syscall`.
* `hijack-fd`: is improved.
    * It supports more architectures.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/hijack-fd.png)
* `format-string-helper` is improved.
    * It supports more printf-like functions.
* `theme` is improved.
    * Supports many colors.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/theme.png)
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/theme-colors-sample.png)
* `reset-cache` is improved.
    * The cache structure within GEF has changed significantly. This command corresponds to them.

### Added features
* `pid`/`tid`: prints pid and tid.
* `filename`: prints filename.
* `fds`: shows opened file descriptors.
* `auxv`: pretty prints ELF auxiliary vector.
    * Supported also under qemu-user.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/auxv.png)
* `argv`/`envp`: pretty prints argv and envp.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/argv-envp.png)
* `dumpargs`: dumps arguments of current function.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/dumpargs.png)
* `vdso`: disassembles the text area of vdso smartly.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/vdso.png)
* `vvar`: dumps the area of vvar.
    * This area is mapped to userland, but cannot be accessed from gdb.
    * Therefore, it executes the assembly code and retrieve the contents.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/vvar.png)
* `gdtinfo`: pretty prints GDT entries. If userland, show sample entries.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/gdtinfo.png)
* `idtinfo`: pretty prints IDT entries. If userland, show sample entries.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/idtinfo.png)
* `tls`: pretty prints TLS area. Requires glibc.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/tls.png)
* `fsbase`/`gsbase`: pretty prints `$fs_base`, `$gs_base`.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/fsbase_gsbase.png)
* `libc`/`ld`/`heapbase`/`codebase`: displays each of the base address.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/base.png)
* `got-all`: shows got entries for all libraries.
* `break-rva`: sets a breakpoint at relative offset from codebase.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/break-rva.png)
* `command-break`: sets a breakpoint which executes user defined command if hit.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/command-break.png)
* `main-break`: sets a breakpoint at `main` with or without symbols, then continue.
    * This is useful when you just want to run to `main` under using qemu-user or pin, or debugging no-symbol ELF.
* `load-break`: breaks if something is loaded.
* `regdump-break`: sets a breakpoint which dumps specified registers if hit.
* `break-if-taken`/`break-if-not-taken`: sets a breakpoint which breaks if branch is taken (or not taken).
* `distance`: calculates the offset from its base address.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/distance.png)
* `fpu`/`mmx`/`sse`/`avx`/`avx512`: pretty prints FPU/MMX/SSE/AVX/AVX512 registers.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/fpu-mmx-sse-avx.png)
* `xmmset`: sets the value to xmm/ymm/zmm register simply.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/xmmset.png)
* `mmxset`: sets the value to mm register simply.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/mmxset.png)
* `exec-until`: executes until specified operation.
    * Supported following patterns of detection.
        * call
        * jmp
        * syscall
        * ret
        * indirect-branch (only x64/x86)
        * all-branch (call || jmp || ret)
        * memory-access (detect just `[...]`)
        * specified-keyword-regex
        * specified-condition (expressions using register or memory values)
        * user-code
        * libc-code
        * secure-world
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/exec-until.png)
* `xuntil`: executes until specified address.
    * It is slightly easier to use than the original until command.
* `add-symbol-temporary`: adds symbol information from command-line.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/add-symbol-temporary.png)
* `errno`: displays errno list or specified errno.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/errno.png)
* `u2d`: shows cast/convert u64 <-> double/float.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/u2d.png)
* `unsigned`: shows unsigned value.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/unsigned.png)
* `convert`: shows various conversion.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/convert.png)
* `addressify`: converts reverse-order hex values to address.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/addressify.png)
* `walk-link-list`: walks the link list.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/walk-link-list.png)
* `hexdump-flexible`: displays the hexdump with user defined format.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/hexdump-flexible.png)
* `hash`: calculates various hashes.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/hash.png)
* `crc`: calculates various CRCs.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/crc.png)
* `base-n-decode`/`base-n-encode`: decodes/encodes various baseN.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/base-n-decode.png)
* `morse-decode`/`morse-encode`: decodes/encodes morse code.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/morse-decode.png)
* `saveo`/`diffo`: saves and diffs the command outputs.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/saveo-diffo.png)
* `memcmp`: compares the contents of the address A and B, whether virtual or physical.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/memcmp.png)
* `memset`: sets the value to the memory range, whether virtual or physical.
* `memcpy`: copies the contents from the address A to B, whether virtual or physical.
* `memswap`: swaps the contents of the address A and B, whether virtual or physical.
* `meminsert`: inserts the contents of the address A to B, whether virtual or physical.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/meminsert.png)
* `strlen`: detects the length of the string.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/strlen.png)
* `is-mem-zero`: checks the contents of address range is all 0x00 or 0xff or not.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/is-mem-zero.png)
* `seq-length`: detects consecutive length of the same sequence.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/seq-length.png)
* `strings`: searches ASCII string from specific location.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/strings.png)
* `xs`: dumps string like `x/s` command, but with hex-string style.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/xs.png)
* `xc`: dumps address like `x/x` command, but with coloring at some intervals.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/xc.png)
* `ii`: is a shortcut for `x/50i $pc` with opcode bytes.
    * It prints the value if it is memory access operation.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/ii.png)
* `version`: shows software versions that gef used.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/version.png)
* `arch-info`: shows architecture information used in gef.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/arch-info.png)
* `context-extra`: manages user specified command to execute when each step.
* `comment`: manages user specified temporary comment.
* `seccomp`: invokes `seccomp-tools`.
* `onegadget`: invokes `one_gadget`.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/onegadget.png)
* `rp`: invokes `rp++` with commonly used options.
* `call-syscall`: calls system call with specified values.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/call-syscall.png)
* `mmap`: allocates a new memory by `call-syscall`.
* `killthreads`: kills specific or all pthread.
* `constgrep`: invokes `grep` under `/usr/include/`.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/constgrep.png)
* `proc-dump`: dumps each file under `/proc/PID/`.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/proc-dump.png)
* `up`/`down`: are the wrapper for native `up`/`down`.
    * It shows also backtrace.
* `time`: measures the time of the GDB command.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/time.png)
* `multi-line`: executes multiple GDB commands in sequence.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/multi-line.png)
* `cpuid`: shows the result of cpuid(eax=0,1,2...).
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/cpuid.png)
* `read-system-register`: reads system register for old `qemu-system-arm`.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/read-system-register.png)
* `read-control-register`: reads control register for kgdb.
* `capability`: shows the capabilities of the debugging process.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/capability.png)
* `dasm`: disassembles the code by capstone.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/dasm.png)
* `asm-list`: lists up instructions. (only x64/x86)
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/asm-list.png)
    * This command uses x86data.js from https://github.com/asmjit/asmdb
* `syscall-search`: searches system call by regex.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/syscall-search.png)
* `dwarf-exception-handler`: dumps the DWARF exception handler information.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/dwarf-exception-handler.png)
* `magic`: displays useful addresses in glibc etc.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/magic.png)
* `dynamic`: dumps the `_DYNAMIC` area.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/dynamic.png)
* `link-map`: dumps useful members of `link_map` with iterating.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/link-map.png)
* `dtor-dump`: dumps some destructor functions list.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/dtor-dump.png)
* `ptr-mangle`: shows the mangled value will be mangled by `PTR_MANGLE`.
* `ptr-demangle`: shows the demangled value of the value mangled by `PTR_MANGLE`.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/ptr-mangle-demangle.png)
* `search-mangled-ptr`: searches the mangled value from RW memory.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/search-mangled-ptr.png)
* `follow`: changes `follow-fork-mode` setting.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/follow.png)
* `smart-cpp-function-name`: toggles `context.smart_cpp_function_name` setting.
* `ret2dl-hint`: shows the structure used by return-to-dl-resolve as hint.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/ret2dl-hint.png)
* `srop-hint`: shows the code for sigreturn-oriented-programming as hint.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/srop-hint.png)
* `sigreturn`: displays stack values for sigreturn syscall.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/sigreturn.png)
* `smart-memory-dump`: dumps all regions of the memory to each file.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/smart-memory-dump.png)
* `load-file`: loads the file into memory.
* `search-cfi-gadgets`: searches CFI-valid (for CET IBT) and controllable generally gadgets from executable area.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/search-cfi-gadgets.png)
* `symbols`: lists up all symbols with coloring.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/symbols.png)
* `types`: lists up all types with compaction.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/types.png)
* `dt`: makes it easier to use `ptype /ox TYPE` and `p ((TYPE*) ADDRESS)[0]`.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/dt.png)
    * This command is designed for several purposes.
        1. When displaying very large struct, you may want to go through a pager because the results will not fit on one screen.
           However, using a pager, the color information disappears. This command calls the pager with preserving colors.
        2. When `ptype /ox TYPE`, interpreting member type recursively often result is too long and difficult to read.
           This command keeps result compact by displaying only top-level members.
        3. When `p ((TYPE*) ADDRESS)[0]` for large struct, the setting of `max-value-size` is too small to display.
           This command adjusts it automatically.
        4. When debugging a binary written in the golang, the offset information of the type is not displayed.
           This command also displays the offset.
        5. When debugging a binary written in the golang, the `p ((TYPE*) ADDRESS)[0]` command will be broken.
           Because the golang helper script is automatically loaded and overwrites the behavior of `p` command.
           This command creates the display results on the python side, so we can display it without any problems.
* `v8`: displays v8 tagged object.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/v8.png)
    * It also loads more commands from latest gdbinit for v8.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/v8-load.png)
* `mte-tags`: displays the MTE tags for the specified address.
    * Supported on ARM64.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/mte-tags.png)
* `iouring-dump`: dumps the area of iouring (only x64).
    * This area is mapped to userland, but cannot be accessed from gdb.
    * Therefore, it executes the assembly code and retrieve the contents.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/iouring-dump.png)
* `reset-bp`: shows and resets all breakpoints.
* `gef arch-list`: displays defined architecture information.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/gef-arch-list.png)
* `gef pyobj-list`: displays defined global python object.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/gef-pyobj-list.png)
* `gef avail-comm-list`: displays a list of commands which are available or not for the current architecture and gdb execution mode.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/gef-avail-comm-list.png)
* `gef set-arch`: sets a specific architecture to gef.
* `gef check-update`: checks for gef updates.
* `binwalk-memory`: scans memory by `binwalk`.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/binwalk-memory.png)
* `filetype-memory`: scans memory by `file` and `magika`.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/filetype-memory.png)
* `sixel-memory`: shows image to terminal by `imagemagick`.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/sixel-memory.png)
* `stdio-dump`: dumps members of stdin/stdout/stderr.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/stdio-dump.png)
* `peek-pageframe`: reads page frame data.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/peek-pageframe.png)
* `peek-pageflags`: reads page flags of a page frame.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/peek-pageflags.png)
* `angr`: finds simple constraints by `angr`.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/angr.png)

### Other
* The category is introduced in `gef help`.
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/gef-help.png)
* Combined into one file (from gef-extra). The following are moved from gef-extras.
    * `current-stack-frame`, `xref-telescope`, `bytearray`, and `bincompare`.
    * This is because a single file is more attractive than ease of maintenance.
* The system-call table used by `syscall-args` is moved from gef-extras.
    * It was updated up to linux kernel 6.13 for each architecture.
* Removed some features I don't use.
    * `$`
    * `ida-interact`
    * `gef-remote`
    * `pie`
    * `pcustom`
    * `ksymaddr`
    * `trace-run`
    * bufferize
    * output redirect
    * `shellcode`
* Many bug fixes / formatting improvements / usability enhancements (made it easy for me to use).

## FAQ
* See [docs/FAQ.md](https://github.com/bata24/gef/blob/dev/docs/FAQ.md).
