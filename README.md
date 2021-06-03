## Install

```bash
# Run with root privileges
wget -q https://raw.githubusercontent.com/bata24/gef/dev/install.sh -O- | sh
```

## Upgrade (replace itself)
```bash
python3 /root/.gdbinit-gef.py --upgrade
```

## Uninstall

```bash
rm -f /root/.gdbinit-gef.py /root/.gef.rc
```

## Added / Improved features

All of these features are experimental. Tested on Ubuntu 18.04 / 20.04 / Debian 10.x.

### qemu-system cooperation
* It works with qemu-system installed with apt, but qemu-6.x is recommended
* `qreg`: prints register values from qemu-monitor (allows to get like `$cs` even under qemu 2.x)
    * It also prints the details of the each bit of the system register when x64/x86
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/qreg.png)
* `msr`: prints MSR (Machine Specific Register) values by embedding/executing dynamic assembly
    * Supported on x64/x86
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/msr.png)
* `pagewalk`: prints pagetables from scanning of physical memory
    * x64 (Supported: PML5T/PML4T)
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/pagewalk-x64.png)
    * x86 (Supported: PAE/Non-PAE)
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/pagewalk-x86.png)
    * ARM64 (Supported: EL0/EL1/EL2/VEL2/EL3)
        * 32bit mode is NOT supported
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/pagewalk-arm64.png)
    * ARM (Cortex-A only, LPAE/Non-LPAE, PL0/PL1)
        * PL2 is NOT supported
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/pagewalk-arm.png)
* `xp`: is a shortcut for physical memory dump
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/xp.png)
* `ksymaddr-remote`: prints kallsyms informations from scanning of kernel memory (heuristic)
    * Supported: the symbol of kernel itself
    * Unsupported: the symbol of kernel modules
    * Supported on x64/x86/ARM64/ARM
    * Supported on both kASLR is enabled or not
    * Unsupported: to resolve no-function address when kernel built as `CONFIG_KALLSYMS_ALL=n`
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/ksymaddr-remote.png)
* `ksymaddr-remote-apply`: applies kallsyms informations obtained with `ksymaddr-remote` to gdb
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/ksymaddr-remote-apply.png)
* `slab`: dumps slab free-list (heuristic)
    * Supported on x64/x86/ARM64/ARM + SLUB
    * Unsupported SLAB, SLOB
    * Supported on both kASLR is enabled or not
    * Supported on both `CONFIG_SLAB_FREELIST_HARDENED` is `y` or `n`
    * Supported on both the vmlinux symbol exists or not
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/slab.png)
* `uefi-ovmf-info`: displays addresses of important structures in each boot phase of UEFI when OVMF is used (heuristic)
    * Supported on x64 only
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/uefi-ovmf-info.png)

### New heap dump features
* `tcmalloc-dump`: dumps tcmalloc free-list (heuristic)
    * For tcmalloc, there are 3 major versions
        1. tcmalloc that is a part of gperftools published in 2005: supported
        2. tcmalloc that is included in chrome mainline: supported
        3. tcmalloc that is maintained in Google Inc. published in 2020: unsupported
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/tcmalloc-dump.png)
* `musl-dump`: dumps musl-libc unused chunks (heuristic)
    * Supported on x64/x86, based on musl-libc v1.2.2
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/musl-dump.png)
* `partition-alloc-dump`: dumps partition-alloc free-list (heuristic)
    * Supported on x64 only
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/partition-alloc-dump.png)

### Other improved features
* Glibc heap commands are improved
    * Thread arena is supported for all heap commands
        * Use `-a` option
    * They print the chunk is in free-list or not
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/heap-if-in-freelist.png)
    * `find-fake-fast`: searches for a memory with a size-like value that can be linked to the fastbin free-list
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/find-fake-fast.png)
    * `visual-heap`: is colorized heap viewer
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/visual-heap.png)
    * `extract-heap-addr`: analyzes tcache-protected-fd introduced from glibc-2.32
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/extract-heap-addr.png)
* `vmmap` is improved
    * It prints meomry map informations even when connecting to gdb stub like qemu-user (heuristic), intel pin and intel SDE
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/vmmap-qemu-user.png)
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/vmmap-pin.png)
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/vmmap-sde.png)
    * It is redirected to `pagewalk` when connecting to gdb stub of qemu-system
* `registers` is improved
    * It also shows raw values of `$eflags` and `$cpsr`
    * It prints current ring for x64/x86 when prints `$eflags` (from `$cs`)
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/registers-x64.png)
    * It prints current exception level for ARM64 when prints `$cpsr`
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/registers-arm64.png)
    * It prints current mode for ARM when prints `$cpsr`
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/registers-arm.png)
* `context` is improved
    * It supports automatic display of system call arguments when calling a system call
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/context-syscall-args.png)
    * It supports automatic display of address and value when accessing memory
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/context-memory-access.png)
    * It supports smart symbol printing for cpp function
        * ex: `std::map<int, std::map<int, int>>` will be replaced by `std::map<...>`
        * command: `gef config context.smart_cpp_function_name true` or `smart-cpp-function-name` (later is used to toggle)
* `telescope` is improved
    * It prints ordinal numbers as well as offsets
    * It prints if there are canary and ret-addr on the target area
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/telescope.png)
    * It supports blacklist address features (to avoid dying when touching the address mapped to the serial device)
* `procinfo` is improved
    * It prints some additional informations
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/procinfo.png)
* `elf-info` is improved
    * It prints Program Header and Section Header
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/elf-info.png)
    * It supports parsing from memory
* `checksec` is improved
    * It prints Intel CET is enabled or not
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/checksec.png)
* `got` improved
    * It prints not only GOT address but also PLT address
    * It scans `.plt.sec` section if Intel CET is enabled
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/got.png)
* `canary` is improved
    * It prints all canary positions in memory
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/canary.png)
* `edit-flags` is improved
    * It prints the meaning of each bit if `-v` option is provided
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/edit-flags-x64.png)
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/edit-flags-arm.png)
        * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/edit-flags-arm64.png)
* `unicorn-emulate` is improved
    * It reads and writes correctly to the address pointed to by `$fs`/`$gs`
* `ropper` is improved
    * It does not reset autocomplete settings after calling imported ropper
* `hexdump` is improved
    * It supports physical memory if under qemu-system
    * It will retry with adjusting read size when failed reading memory
* `patch` is improved
    * It supports physical memory if under qemu-system
* `search-pattern` is improved
    * It supports physical memory if under qemu-system
    * It supports aligned search
    * It supports hex string specification
    * It also searches utf-16 string if target string is ascii

### Other new features
* `pid`: prints pid
* `filename`: prints filename
* `auxv`: pretty prints ELF auxiliary vector
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/auxv.png)
    * Supported also under qemu-user (heuristic)
* `argv`: pretty prints argv
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/argv.png)
* `envp`: pretty prints envp
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/envp.png)
* `gdtinfo`: pretty prints GDT sample
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/gdtinfo.png)
* `tls`: pretty prints `$fs` base / `$gs` base
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/tls.png)
* `magic`: is useful addresses resolver in gilbc
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/magic.png)
* `libc`/`ld`/`heapbase`/`codebase`: prints each of the base address
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/base.png)
* `mmx`/`sse`/`avx`/`fpu`: pretty prints MMX/SSE/AVX/FPU registers 
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/mmx-sse-avx-fpu.png)
* `sysreg`: pretty prints system registers under ARM/ARM64
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/sysreg.png)
* `exec-until`: executes until specific operation
    * Supported on x64/x86/ARM64/ARM for call/jmp/syscall/ret/mem-access/specific-keyword
* `add-symbol-temporary`: adds symbol information from command-line
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/add-symbol-temporary.png)
* `errno`: prints errno list or specific errno
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/errno.png)
* `u2d`: is cast/transformation u64 <-> double
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/u2d.png)
* `hash-memory`: calculations hash
    * Supported: md5, sha1, sha224, sha256, sha384, sha512, crc16, crc32, crc64
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/hash-memory.png)
* `memcmp`: compares the contents of address A and B, whether virtual or physical
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/memcmp.png)
* `is-mem-zero`: checks the contents of address range is all zero or not
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/is-mem-zero.png)
* `byteswap`: is transformation little-endian <-> big-endian
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/byteswap.png)
* `pdisas`: is a shortcut for `cs-dis $pc LENGTH=50 OPCODES`
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/pdisas.png)
* `ii`: is a shortcut for `x/50i $pc`
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/ii.png)
    * It prints the value if memory access operation
    * tips: gef has 3 types to print instructions. `context`, `pdisas`, and `ii`
* `version`: shows software version that gef used
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/version.png)
* `follow`: changes `follow-fork-mode` setting
* `smart-cpp-function-name`: toggles `context.smart_cpp_function_name` setting
* `seccomp-tools`: invokes `seccomp-tools`
* `onegadget`: invokes `one_gadget`
* `ls`/`cat`: invokes `ls`/`cat` directly
* `constgrep`: invokes `grep` under `/usr/include`
* `rp`: invokes `rp++`

### Other
* Replace the unicode character to ascii
    * ex: &#x27a4; to `>`
    * ex: &#x2713; to `OK`
* The category introduced in `gef help`
    * ![](https://raw.githubusercontent.com/bata24/gef/dev/images/gef-help.png)
* Combined into one file (from gef-extra)
    * `peek-pointers`, `current-stack-frame`, `xref-telescope`, `bytearray`, `bincompare`, and `ftrace` are moved from gef-extras
* The system-call table used by `syscall-args` is moved from gef-extras
    * It was updated up to linux kernel 5.12.8 (only x64/x86/ARM64/ARM yet)
* Removed some features I don't use
    * `ida-interact`, `gef-remote`, `pie`, and `pcustom`
* Many bugs fix / formatting / made it easy for me to use
