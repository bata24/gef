# FAQ

## Table of Contents
- [About GEF's Files or Directories](#about-gefs-files-or-directories)
- [About the Installation](#about-the-installation)
- [About the Host Environment](#about-the-host-environment)
- [About the Guest (Debugged) Environment](#about-the-guest-debugged-environment)
- [About GEF Settings](#about-gef-settings)
- [About Commands](#about-commands)
- [About the Internal Mechanism](#about-the-internal-mechanism)
- [About the Python Interface](#about-the-python-interface)
- [About the Development Schedule](#about-the-development-schedule)
- [About Reporting, etc.](#about-reporting-etc)
- [Other Memo (Japanese)](#other-memo-japanese)


# About GEF's Files or Directories

## Where is `gef.py`?
By default, GEF (`gef.py`) is placed at `/root/.gef/gef.py`.

GEF is primarily a single file (`gef.py`). Optional configuration and helper files may accompany it.

## What is `~/.gef.rc`?
This is the GEF configuration file. It is not present by default.

Executing the `gef save` command saves the current settings to disk (`~/.gef.rc`).
The next time GEF starts, it will automatically load this file and apply the saved settings.
This includes the current values of items configurable with `gef config` and user-defined command aliases.

## What is `~/.gdbinit`?
This is the command file that GDB will execute when it starts up.

By including the following command to load `gef.py`, GEF will be loaded automatically.
There are two ways to load GEF from `.gdbinit`; either one works.
```
# New style
python sys.path.insert(0, "/root/.gef"); from gef import *; Gef.main()

# Old style
source /root/.gef/gef.py

# Another old style
source /root/.gdbinit-gef.py  # In the old installer, GEF was located here
```

Notes:
- The former (new style) imports GEF using Python. Because a `*.pyc` file is generated and cached, subsequent startups are faster. This is the default setting in recent versions of GEF.
- The latter (old style) is the traditional method, where GEF is loaded directly. It takes longer to load each time, but the command is simpler.

## What is `/tmp/gef`?
This is the directory where GEF temporarily stores files.

Since it is used for caching, deleting it does not cause any issues.
It will be created automatically the next time GEF starts.

The variable `GEF_TEMP_DIR` is defined in `gef.py` and can be changed if necessary.

## What is `install-uv.sh`?
This is the new installer that creates and uses a Python virtual environment (`venv`).

It installs the same packages as `install.sh`.
The key difference is that Python packages are installed into the virtual environment (`venv`).

By default, it installs into `/root/.gef/.venv-gef`.
External tools such as `rp++`(`rp-lin`), `seccomp-tools`, etc. are also installed under this directory (`/root/.gef/.venv-gef/bin`).

Usage:
```
# Run the following commands as `root` or `sudo`
wget -q https://raw.githubusercontent.com/bata24/gef/dev/install-uv.sh -O- | sudo sh
```

## What is `install.sh`?
This is the old installer that was used before the `uv`-based installation became available.

This installer is not currently recommended, but it still works.

Usage:
```
# Run the following commands as `root` or `sudo`

# On Ubuntu 23.04 or later, global Python package installation via pip3 is restricted.
# Use the --break-system-packages option.
wget -q https://raw.githubusercontent.com/bata24/gef/dev/install.sh -O- \
| sed -e 's/pip3 install/pip3 install --break-system-packages/g' | sudo sh

# For Ubuntu 22.10 or earlier
wget -q https://raw.githubusercontent.com/bata24/gef/dev/install.sh -O- | sudo sh
```

## What is `install-minimal.sh`?
This is an installer for running GEF in restricted environments where required packages cannot be installed due to various limitations.

Most core features work, but commands that depend on extra Python packages or external tools will be unavailable.

Usage:
```
# Run the following commands as `root` or `sudo`
wget -q https://raw.githubusercontent.com/bata24/gef/dev/install-minimal.sh -O- | sudo sh
```

Notes:
- The process is straightforward: download `gef.py`, place it in the appropriate location, and add a line to `.gdbinit` to load it. You can also do the same thing manually.
- Because it does not install any Python packages, it does not create a `venv`.

## What is `gef.venv.conf`?
This is a path information file required by GEF if you installed GEF using `install-uv.sh`.
It is not generated if you use `install.sh` or `install-minimal.sh`.
Place this file in the same directory as `gef.py`.

It contains three pieces of path information:
- `GEF_VENV_GEM_HOME`
    - Sets `GEM_HOME` so Ruby `gem`-installed tools can be discovered and used by GEF.
- `GEF_VENV_SYS_PATH`
    - By default, GEF searches globally installed Python packages.
    - Prepend this path to `sys.path` so that packages inside the `venv` take precedence.
- `GEF_VENV_BIN_PATH`
    - By default, GEF searches for executables using the `$PATH` environment variable (the actual process is a bit more complicated).
    - GEF will prepend the specified path to the search directories before searching.


# About the Installation

## How many ways are there to install GEF?
There are three installers.

- `uv`-based install
    - This is the installation method provided by `install-uv.sh`.
    - This uses `uv` to install Python packages into an isolated environment.
    - This is a full installation, so you can use all the features that GEF provides.
    - This is the currently recommended installer for GEF, because it is faster than the other methods.
- Minimal install
    - This is the installation method provided by `install-minimal.sh`.
    - Simply download `gef.py` and place it in the appropriate location.
    - Because this method is very simple, it can also be performed manually.
- Normal install
    - This is the installation method provided by `install.sh`.
    - This is a full installation, so you can use all the features that GEF provides.
    - This uses `python3-pip` to install Python packages globally.
    - This installer is not currently recommended, but it still works.
    - This method was used before the `uv`-based installation became available.

For an explanation of each installer, see [About GEF's Files or Directories](#about-gefs-files-or-directories).

## How to change the location of GEF? / How can I run GEF as a non-`root` user?
This is not officially supported; proceed at your own risk. Future updates may break this workflow.

```
# First, download GEF install script
wget -q https://raw.githubusercontent.com/bata24/gef/dev/install-uv.sh -P /tmp

# apt-get install as root
sudo apt-get update
sudo apt-get install <needed-package>   # see /tmp/install-uv.sh

# 1. replace GDBINIT_PATH and GEF_DIR as you wanted
# 2. remove root user check
# 3. remove apt-get install
vim /tmp/install-uv.sh

# install
sh /tmp/install-uv.sh

# Delete /tmp/gef directory (if it exists)
sudo rm -rf /tmp/gef
```

Alternative simple method (no external tools; simple loading):

```
# Download
wget -q https://raw.githubusercontent.com/bata24/gef/dev/gef.py -O ~/.gdbinit-gef.py

# Add path to .gdbinit
echo "source $HOME/.gdbinit-gef.py" >> ~/.gdbinit
```

Notes:
- GEF is designed to have as few dependencies as possible. Many commands should work with just `gef.py` without any additional external tools.
- If you do not install external tools, the features that will not be available are listed below.

## If I do not install external tools, which commands will no longer be available?
The following is a breakdown. It may not be comprehensive.

To use these commands fully, you need to manually install the necessary packages and tools.

|GEF command/feature|Required apt package|Required python3 package|Required other tools|
|:---|:---|:---|:---|
|(`gef`)|`gdb` or `gdb-multiarch`|-|-|
|`got`|`binutils` (`objdump`, `readelf`)|-|-|
|`got --cppfilt`|`binutils` (`c++filt`)|-|-|
|`add-symbol-temporary`|`binutils` (`objcopy`)|-|-|
|`ksymaddr-remote-apply`|`binutils` (`objcopy`)|-|-|
|`ksymaddr-remote --vmlinux-file`|`binutils` (`nm`)|-|-|
|`qemu-device-info`|`binutils` (`nm`)|-|-|
|`rp`|`binutils` (`nm`)|-|`rp++`|
|`binwalk-memory`|`binwalk`|-|-|
|`diffo colordiff`|`colordiff`|-|-|
|`diffo git-diff`|`git`|-|-|
|`sixel-memory`|`imagemagick`|-|-|
|`sixel-memory -b`|-|`pillow`, `pyzbar`|-|
|`vdump`|`imagemagick`|-|-|
|`ktask -S`|-|-|`seccomp-tools`|
|`seccomp-tools`|-|-|`seccomp-tools`|
|`onegadget`|-|-|`one_gadget`|
|Progress Indicator|-|`tqdm`|-|
|`angr`|-|`angr`|-|
|`asm-list`|-|`capstone`|-|
|`capstone-disassemble`|-|`capstone`|-|
|`dasm`|-|`capstone`|-|
|`i8086` mode|-|`capstone`|-|
|`unicorn-emulate`|-|`capstone`, `unicorn`, `setuptools`(python 3.12+)|-|
|`heap try-free`|-|`capstone`, `unicorn`, `setuptools`(python 3.12+)|-|
|`heap try-malloc`|-|`capstone`, `unicorn`, `setuptools`(python 3.12+)|-|
|`heap try-realloc`|-|`capstone`, `unicorn`, `setuptools`(python 3.12+)|-|
|`heap try-calloc`|-|`capstone`, `unicorn`, `setuptools`(python 3.12+)|-|
|`asm`|-|`keystone-engine`|-|
|`base-n-decode`|-|`codext`|-|
|`base-n-encode`|-|`codext`|-|
|`crc`|-|`crccheck`|-|
|`hash`|-|`pycryptodome`|-|
|`uefi-ovmf-info`|-|`crccheck`|-|
|`filetype-memory`|`file`|`magika`|-|
|`ropper`|-|`ropper`|-|
|`vmlinux-to-elf-apply`|-|`vmlinux-to-elf`|-|

## Why are there so many packages installed when running `apt-get install` in the installer?
Because the `binwalk` package has a large number of dependencies.

If you do not use the `binwalk-memory` command, you do not need to install `binwalk` (please modify the installer manually).

# About the Host Environment

## Does GEF work properly on operating systems other than Ubuntu?
Yes, it generally works on most standard Linux distributions; however, not every command is validated on every distribution.

I have used it on Debian, and some users are running it on Arch Linux.
It also seems to be working fine on WSL2 (Ubuntu) so far.
However, I have not confirmed that all commands work correctly.

## Will this GEF work as a plugin for `hugsy/gef`?
No, it does not work as a plugin. It replaces `hugsy/gef`.

Compatibility with `hugsy/gef` has already been lost, as well as with `hugsy/gef-extras`.
It should be considered an entirely separate product.

Similarly, this GEF cannot be used at the same time as `peda` or `pwndbg`.
Make sure you only load one of them.

## GDB will not load GEF.
Start GDB as the `root` user or with `sudo`.
By default, GEF is installed under `/root/.gef`, so non-`root` sessions will not find it unless you change the install paths or update your `.gdbinit` to point to the actual location.


## GDB still does not load GEF, even as the `root` user.
It is likely that your GDB does not support integration with `python3`.

This can happen if you are not using the GDB provided by Ubuntu's `apt` package manager. For example:
- You built it yourself from source code
- You are using a version that someone else prepared for a specific architecture

Consider rebuilding GDB from the latest tarball or from the Git repository.

- From the latest tarball:
    - Download latest tarball from https://ftp.gnu.org/gnu/gdb/
    ```
    tar xf gdb-16.3.tar.xz && cd gdb-16.3
    ./configure --enable-targets=all --with-python=/usr/bin/python3
    make && make install
    ```
- From Git:
    ```
    apt install -y libdebuginfod-dev libreadline-dev
    git clone --depth 1 https://github.com/bminor/binutils-gdb && cd binutils-gdb
    ./configure --disable-{binutils,ld,gold,gas,sim,gprof,gprofng} --enable-targets=all \
    --with-python=/usr/bin/python3 --with-debuginfod --with-system-{zlib,readline}
    make && make install
    ```

## When debugging with GDB, how can I display the source code of preinstalled libraries and commands?
For Ubuntu 22.10 and later, it is recommended to use `debuginfod`.

- Enable `debuginfod` (Ubuntu 22.10 and later)
    ```
    export DEBUGINFOD_URLS="https://debuginfod.ubuntu.com"
    echo "set debuginfod enabled on" >> ~/.gdbinit
    ```

- If you are unable to use `debuginfod`, please set up the symbols manually.
    ```
    # Not necessary if debuginfod is enabled
    apt install libc6-dbg
    echo "set debug-file-directory /usr/lib/debug" >> ~/.gdbinit
    ```

However, `debuginfod` often does not provide `glibc` source files.
Fetch and place the `glibc` sources locally as shown below.

- Get the `glibc` source
    ```
    # Ubuntu 24.04 or later
    sed -i -e 's/^Types: deb$/Types: deb deb-src/g' /etc/apt/sources.list.d/ubuntu.sources

    # Ubuntu 23.10 or before
    sed -i -e 's/^# deb-src/deb-src/g' /etc/apt/sources.list

    # common
    cd /usr/lib/debug && apt update && apt source libc6
    echo "directory /usr/lib/debug/glibc-2.39" >> ~/.gdbinit
    # You need to adjust the version for your environment.
    ```


# About the Guest (Debugged) Environment

## What Linux kernel versions does GEF support as guests in qemu-system?
Most commands have been validated on kernels from 3.x up to 6.17.x. Newer kernels may work but are not fully validated.

However, I have not verified every kernel version.
For example, certain symbols in some versions may not be supported by heuristic symbol detection.
Also, the structure may differ depending on the build configuration and the compiler used to build the kernel.
Therefore, there may be environments where GEF does not work.
If you encounter any issues, please report them on the issue page.

## Is there a way to get a prebuilt kernel for each version?
I use [https://kernel.ubuntu.com/](https://kernel.ubuntu.com/mainline).

Download the desired `linux-image-unsigned-*_amd64.deb` and extract `/boot/vmlinuz-*` from it (e.g., with `dpkg-deb -x`).
No filesystem image is provided. Please use one created with `buildroot` or one provided in past CTF challenges.

Download the `linux-modules-*_amd64.deb` package for `System.map` and `config`.

## Will each GEF command be more accurate if I have `vmlinux` with debug symbols?
Let's consider debug information and debug symbols separately.

- Debug information
    - No, the presence or absence of debug information in `vmlinux` does not impact GEF's functionality or behavior.
        - GEF performs its own heuristic structure member detection in each command.
- Debug symbols
    - Yes, you can use `ksymaddr-remote --vmlinux-file <vmlinux_path>`.
        - GEF internally uses the addresses resolved with `ksymaddr-remote`, and these results are cached.
        - Therefore, by specifying the `vmlinux` file, the results of `ksymaddr-remote` can be replaced with accurate values and cached.

## Does GEF support i386 16-bit mode (real mode)?
Yes, GEF supports real mode experimentally.

Use `qemu-system-i386`, and do NOT use `qemu-system-x86_64`.
Explicitly specify the i8086 architecture before connecting: `gdb -ex 'set architecture i8086' -ex 'target remote localhost:1234'`.

GEF automatically handles transitions between 16-bit real mode and 32-bit protected mode, but expect limitations compared to 32/64-bit workflows.

## Does GEF support ARM Cortex-M?
Yes, GEF supports ARM Cortex-M.

You can debug microcontrollers, but the memory map cannot be enumerated via GDB; consult vendor documentation or SVD files for layout details.

## Is it possible to debug userland with GEF when using qemu-system?
Partially, yes.

I think it can be useful when you want to trace before and after a system call.
However, of course, I do not recommend continually debugging userland with qemu-system.
This is because many commands are restricted for various reasons.
Consider setting up `gdbserver` in the guest and connecting from the outside.

Note:
- If KPTI is enabled, many kernel-related commands cannot be used in userland. This is because most memory access to kernel space is unavailable if KPTI is enabled.

## How do I break in userland when using qemu-system?
Use a hardware breakpoint.

When execution is stopped in the kernel, first ensure you are in the intended process context. If so, you can set a `break *ADDRESS` as usual.
If execution stopped in the kernel context of a different user process than you expected, or in a kernel thread like `swapper/0`, the virtual address of the process you want is not mapped.
For this reason, software breakpoints that embed `0xcc` in virtual memory cannot be used in some situations.
However, hardware breakpoints can be used without any problems.

## Does GEF support debugging the Android kernel?
Yes, it is supported, but not fully.

When I tried using `Android Studio`, most commands seemed to work.
- I used `Android Studio` on Windows and connected from Linux.
- Refer to [docs/SUPPORTED-MODE.md](SUPPORTED-MODE.md) for the commands I used.

However, the QEMU in `Android Studio` is based on an older version, 2.12.0, and seems to have compatibility issues with recent GDB versions (16.x and later).
Specifically, repeated memory reads may cause QEMU's GDB stub to return incorrect results.
This is especially noticeable for commands that perform repeated memory access, such as `ktask` and `kchecksec`.

## Does GEF support debugging Android userland binaries?
Yes, it is supported, but not fully.

When I tried using `Android Studio`, most commands seemed to work.
- I used `Android Studio` on Windows and connected from Linux.
- Refer to [docs/SUPPORTED-MODE.md](SUPPORTED-MODE.md) for the commands I used.

However, Android does not use glibc (it uses the Bionic C library).
Therefore, be aware that all `glibc`-specific commands, such as the `heap` command, cannot be used.

## Does GEF support TEE OSs other than OP-TEE?
No, GEF does not support them.


# About GEF Settings

## I prefer the AT&T syntax.
You can set the AT&T syntax for each session using the `set disassembly-flavor att` command.

Alternatively, since the `set disassembly-flavor intel` command is executed in the main function of GEF, you may want to comment it out.
However, as GEF is not optimized for AT&T syntax parsing, some commands may not function correctly.
If you find a case where it does not work, please report it on the issue page.

## I don't like the color scheme.
Customize it using the `theme` command, then run `gef save`.
This will save the configuration to `~/.gef.rc`.

Another option is to disable colors. Try `gef config gef.disable_color True`.

## I don't want to add `-n` to every command to disable pager.
To permanently disable the pager, use the command `gef config gef.always_no_pager True` followed by `gef save`.


# About Commands

## Which command should I start with when debugging the kernel?
Try `pagewalk` , `ks-apply`, and `kchecksec`.
After that, try `slub-dump`, `ktask` and `ksysctl` as well.

Other commands are less important, so check them with `gef help` if necessary.

## Is it possible for GEF to re-display the results of a command (for using the `less` pager)?
In general, no.

If you need to keep output while the `less` pager is active, use `|$cat > /tmp/foo.txt`.

Alternatively, set `gef config gef.keep_pager_result True` and then `gef save`.
From the next time onwards, temporary files will no longer be deleted.

## Is it possible for GEF to pass the result of a command to a shell command?
Yes, you can use the built-in `pipe` command.

For example, `pipe elf-info -n | grep .data` or `|pdisas | grep call`.

## `ktask` (or other kernel-related commands) does not work.
The kernel you are debugging may have been built with `CONFIG_RANDSTRUCT=y`.

In this case, except for a few commands, most will not work correctly.
Currently, at least the following commands do not work:
- `ktask`
- `kmod`
- `kbdev`
- `kcdev`
- `kops`
- `kpipe`
- `ksysctl`
- `kmalloc-tracer`
- `kmalloc-allocated-by`
- `kfiles`
- `kregs`
- `ksighands`
- `kpcidev`
- `knamespaces`
- `kipcs`
- `kfilesystems`

If it does not work properly even though `CONFIG_RANDSTRUCT=n`, GEF may be failing to parse due to a change in `struct task_struct` or similar.
If you think there is a problem with GEF, please report it on the issues page.

## The `vmmap` command does not recognize options.
Try the `pagewalk` command.

When connected to qemu-system or VMware's GDB stub, the `vmmap` command is simply redirected to the `pagewalk` command.
All options are ignored in this case.
If you want to use options, please use the `pagewalk` command instead of the `vmmap` command.

## The `vmlinux-to-elf-apply` command causes an error when creating an ELF file.
Please update `vmlinux-to-elf` to the latest version.

If the problem persists, try using the `ks-apply` command.
The logic is slightly different, so it might work.
If it still does not work, please report it on the issue page.

## If I have a `vmlinux` with debuginfo, how can I use `ks-apply`?
The `ks-apply` command is unnecessary.
Run `kload <vmlinux_path>` (The `kload` command is an easy-to-use wrapper around the `add-symbol-file` command. This automatically applies `kbase` address.)

Optionally, also run `ksymaddr-remote --vmlinux-file <vmlinux_path>`.

|Component|How GDB uses it|How GEF uses it|
|:---|:---|:---|
|`vmlinux` debuginfo|- Loaded via `kload` command<br>- Essential for source-level debugging|- Unused|
|`vmlinux` symbols|- Loaded via `kload` command<br>- Provides kernel symbol resolution|- Accessible via `ksymaddr-remote --vmlinux-file <path>`<br>- This overrides the result of parsing `kallsyms` in memory<br>- Addresses will be automatically rebased|
|Memory-resident `kallsyms`|- Not available by default<br>- Accessible via `ks-apply` command|- Accessible after `ksymaddr-remote` command<br>- Used by various GEF commands internally|

## The kernel-related commands are unstable; sometimes they work fine, sometimes they don’t. / The output of `ksymaddr-remote` seems odd.
This may be due to the GEF's caching mechanism.

GEF resolves kernel symbols using the `ksymaddr-remote` command.
This command caches the offsets (needed for parsing) under the `/tmp/gef` directory.
At that time, it uses the kernel version string (its hash) as the cache key.

Because of this, in a situation like following, you may encounter an issue where the wrong cache is used.
- You have built and debug multiple kernels with slightly different build configs (same kernel version)

To resolve this, after attaching with GDB, execute either of the following:
- `gef reset-cache --hard` (clears the cache)
- `ks -rv` (resolves symbols ignoring the cache)
    - Once symbols are resolved, it remains in effect for the duration of that GDB (GEF) debug session.

## The `got` command does not display PLT addresses.
This problem is probably caused by an outdated version of `binutils`.

The `got` command uses `objdump` internally to obtain the PLT addresses.
However, with certain combinations of `binutils` and `glibc` versions, `objdump` does not display the PLT addresses.

The currently known combinations are as follows:
- `binutils 2.38` (Ubuntu 22.04 default) + `glibc 2.37 or later`

This problem occurs when you try to use a newer `glibc` in an Ubuntu 22.04 environment using `patchelf` etc.
The workaround is to build and install a newer version of `binutils` from source code.

## Can I switch to a mode that references physical memory?
Yes, when using qemu-system. Switch with `pi enable_phys()` and revert with `pi disable_phys()`.
GEF uses this internally; if a command is interrupted mid-execution, you may need to revert manually.

## The `magic` command produces few valid results.
This is because libc symbols are not loaded.

Unlike kernel symbols, userland symbols do not undergo heuristic detection (with some special exceptions).
Therefore, missing symbols may not be detected by the `magic` command.

If you are referring to system-wide `glibc`, you can resolve this with the following steps:
1. Install the symbols with `apt install libc6-dbg`.
2. Add `set debug-file-directory /usr/lib/debug` to `~/.gdbinit`.

## The command to get the source (e.g., `ptr-mangle --source`) does not work.
Do not use `~` in paths that point to the `gef.py` directory in `.gdbinit`.

Python’s `inspect` may not expand tildes reliably; use absolute paths instead.
I encountered this behavior in Python 3.9.2 on Debian 11.

## When using qemu-user, an error occurs when continuing execution.
Is the error something like this?
```
...
dwarf2/dwz.c:188: internal-error: dwarf2_read_dwz_file: Assertion `is_main_thread ()' failed.
A problem internal to GDB has been detected,
further debugging may prove unreliable.
----- Backtrace -----
...
```
If so, this is caused by the `continue-for-qemu-user` command.
This problem occurs only when the configuration option `continue_for_qemu_user.use_fork` is set to `False`.

`continue-for-qemu-user` is a wrapper for the `c`(`continue`) command that allows `Ctrl+C` to be accepted even during `continue` under `qemu-user`.
On some architectures, this wrapper may not work properly when running dynamically linked binaries with `qemu-user`.

There are two ways to work around this:
- Use the `main-break` command to reach `main` once; after that, this error will no longer occur.
- Use the `continue` command instead of the `c` command (but `Ctrl+C` will not work).


# About the Internal Mechanism

## How does GEF implement kernel analysis-related commands without symbols?
Internally, this process consists of several steps:
1. Enumerate memory map information from the page table structure.
2. Detect the `.rodata` area of the kernel from the memory map information.
3. Scan `.rodata` to identify the kernel version.
4. Parse the structure of `kallsyms` in `.rodata` and obtain all "symbol and address" pairs.
5. If global variable symbols are available at this point, use them (= `CONFIG_KALLSYMS_ALL=y`).
    - If not, GEF disassembles the function that uses the specified global variable.
    - By parsing the result, GEF obtains the address of the required global variable.
    - This is implemented in `KernelAddressHeuristicFinder` and `KernelAddressHeuristicFinderUtil` classes.
6. Detect the offset of the structure member, if necessary.
    - To identify it heuristically, GEF uses facts such as whether a value in memory is an address or whether a structure in memory has a specific layout.
    - At this time, GEF takes into account the presence or absence of members and changes in their order due to differences in kernel versions.
7. Parse and display the value in memory using all the information detected so far.

As you can see, this does not work well if structure members are arranged randomly (`CONFIG_RANDSTRUCT=y`).
Also, depending on the assembly output by the compiler, it may not be possible to parse correctly.

## How does GEF achieve the conversion from `page` to `virt` (or `phys`)?
GEF achieves this by using the parsed results of the SLUB free list.

If you are interested in this question, you probably know how difficult this conversion formula is.
As you can see, this conversion (`page <-> virt`) is very difficult.

This is because several values are needed to convert `page` to `virt` (or vice versa), two of which are hard to obtain without symbols and type information:
- `vmemmap`
- `sizeof(struct page)`

I concluded that the only way to get these is to calculate them backwards from valid `page` and `virt` pairs.

These pairs can be found with a very high probability while parsing the SLUB structure.
Therefore, GEF calls the `slub-dump` command internally and temporarily, then calculates these values from the result.

This is the reason why the first time the `page2virt` command runs, it takes a long time: it parses the page tables, identifies function symbols, and internally calls `slub-dump` twice.

Note:
- The `slub-dump` command itself uses the `page` to `virt` conversion function as well, resulting in a circular reference. GEF avoid this problem by adding an option to skip this (`--skip-page2virt`).


# About the Python Interface

## Can I access each GEF command or alias instance from `python-interactive`?
Yes, you can access them via `GCI` or `GAI`.

For example, `pi GCI["vmmap"]` or `pi GAI["us"]`.
- `GCI` stands for Gef Command Instances.
- `GAI` stands for Gef Alias Instances.

## The class name `KernelAddressHeuristicFinder` is too long.
You can access it using `KF`.

For example, use `pi KF.get_slab_caches()` instead of `pi KernelAddressHeuristicFinder.get_slab_caches()`.

## Can I revert the output of `python-interactive` back to decimal from hex?
Yes, you can do so by executing `pi hexoff()`.

## How can I get the instruction object?
You can get the instruction object with `pi get_insn(addr=None)`.

There are also similar functions. Here is the list:
- `get_insn(addr=None)`
- `get_insn_next(addr=None)`
- `get_insn_prev(addr=None)`

## Are there any other globally accessible functions that are useful?
- Memory access
    - `write_memory(addr, data)`, `read_memory(addr, length)`
    - `is_valid_addr(addr)`
    - `read_int_from_memory(addr)`
    - `read_cstring_from_memory(addr, max_length=None)`
    - `read_physmem(paddr, size)`, `write_physmem(paddr, data)`
- Register access
    - `get_register(regname, use_mbed_exec=False, use_monitor=False)`
- Other
    - `String.str2bytes(x)`, `String.bytes2str(x)`
    - `slicer(data, n)`, `slice_unpack(data, n)`
    - `p8`, `p16`, `p32`, `p64`
    - `u8`, `u16`, `u32`, `u64`, `u128`

If you want the complete list, run `gef pyobj-list`.

## I want to add a command. How do I get started?
Copy and paste the `TemplateCommand` class and edit it as you like.

Here are some notes:
- Class name
    - Rename the newly added command class to any name you like.
    - Make sure it ends with `...Command`.
- Inheritance
    - Make sure you inherit from the `GenericCommand` class.
    - This is required for the command to be registered.
- Important attributes
    - `_cmdline_`: used to invoke the command.
    - `_aliases_`: used to create command aliases.
    - `_category_`, `_syntax_`, `_example_` and `_note_`: used by `gef help`.
    - `_repeat_`: enables command repetition.
- `__init__()`
    - This method is executed only once, when GEF starts.
    - There is usually no need to override this method.
    - Delete it if you do not need to do anything special.
- `do_invoke()`
    - It is important to override this method.
    - When a command is executed, it starts from this method.
- Command arguments
    - They should be handled with the `argparse` module.
    - They are managed by the `parse_args` decorator of the `do_invoke()` method.
- Command execution conditions
    - Add decorators to the `do_invoke()` method as needed.
    - You can check the list of available decorators with `gef pyobj-list`.
- Other
    - Use the `gef_print()` function instead of the `print()` function whenever possible.
    - The function named `complete()` is reserved.

## `pi current_arch` is always `None`.
Use `pi import gef; gef.current_arch`, or load GEF using the old style.

This issue occurs when GEF is loaded using the new style (`python sys.path.insert(0, "/root/.gef"); from gef import *; Gef.main()`).
The root cause is that `current_arch` is initially `None`, and during `import`,
its value is copied and turned into a global variable, so it remains `None`.

If you need to access the latest value, explicitly run `pi import gef` and access it as `gef.current_arch`,
or load GEF using the old style (`source /root/.gdbinit-gef.py`).


# About the Development Schedule

## Are there any plans to support kernels for other architectures?
There are no plans.

## Are there any plans to support more architectures with qemu-user?
Yes. However, it is becoming difficult to find new targets to support.

This is because three things are required:
1. Toolchain
    - `linux-headers`, `binutils`, `gcc`, `glibc` (or `uClibc`) are needed.
    - A prebuilt tarball is preferred.
2. Qemu-user
    - It needs an implementation of GDB stub.
3. GDB
    - It needs `python3` support.


# About Reporting, etc.

## After upgrading GEF, it stopped working.
The configuration file format may have changed. Try renaming `~/.gef.rc` (for the `root` user this is `/root/.gef.rc`).

## I found a bug.
Please feel free to report it on the issue page. I will respond as soon as possible.

## Can you please add this feature? / I don't like a certain feature, so please fix it.
I will consider it, so please report it on the issue page.

However, this is a personal project, so I have the final decision. I appreciate your understanding.

## What information should I provide when reporting an issue?
Please provide a screenshot or a copy of the terminal output when the issue occurred.

- Additionally, include the results of the `gef version` and `gef status` commands.
- If the issue is related to kernel debugging, please also provide your environment files (such as `run.sh`, `bzImage`, etc.) or information on where they can be obtained.

## Is it okay to fork and modify?
Yes, please follow the license terms and preserve copyright and attribution notices.


# Other Memo (Japanese)
- Why I decided to make this
    - [gefを改造した話](https://hackmd.io/@bata24/rJVtBJsrP)
- The story behind each command, etc.
    - [bata24/gefの機能紹介とか](https://hackmd.io/@bata24/SycIO4qPi)
- The story behind each command, etc. 2024 Edition
    - [bata24/gefの機能紹介とか 2024](https://hackmd.io/@bata24/SJOzjzqQ1e)
