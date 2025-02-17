# Supported mode

## With docker
* Usage
    * Attach from outside of docker as `gdb-multiarch /PATH/TO/BINARY -p PID`.
        * PID refers to the PID that can be seen by the host.
* Supported architectures
    * Host
        * x86 and x64
        * Maybe ARM and ARM64
* Note
    * Of course, you can also install and use GEF inside docker.
    * However, the `--privileged` option is required when `docker run` or `docker exec`.

## With qemu-system
* Usage
    * Start qemu-system with the `-s` option for listening on `localhost:1234`.
        * If you want to change the listening port, use like `-gdb tcp::9876` option.
    * Attach with `gdb-multiarch -ex 'target remote localhost:1234'`.
    * Or `gdb-multiarch -ex 'set architecture TARGET_ARCH' -ex 'target remote localhost:1234'` (for old qemu).
* Supported architectures
    * Host
        * x64
    * Guest
        * x86, x64, ARM and ARM64
        * i8086 (16-bit) is supported experimentally.
* Note
    * Most commands should work fine unless `CONFIG_RANDSTRUCT=y`.
    * It works with any version qemu-system, but latest version is recommended.
    * It is preferable to run qemu-system on `localhost`.
        * If you run qemu-system on remotely (another host), you can not handle SecureWorld's memory.
    * See [docs/FAQ.md](https://github.com/bata24/gef/blob/dev/docs/FAQ.md) for more information.

## With qemu-user
* Usage
    * Start qemu-user with the `-g 1234` option for listening on `localhost:1234`.
    * Attach with `gdb-multiarch /PATH/TO/BINARY -ex 'target remote localhost:1234'`.
    * Or `gdb-multiarch -ex 'set architecture TARGET_ARCH' -ex 'target remote localhost:1234'` (for old qemu).
* Supported architectures
    * Host
        * x64
    * Guest (ELF)
        * See [docs/QEMU-USER-SUPPORTED-ARCH.md](https://github.com/bata24/gef/blob/dev/docs/QEMU-USER-SUPPORTED-ARCH.md)
* Note
    * It works with any version qemu-user, but latest version is recommended.
        * This is because from qemu-user 8.1, `info proc mappings` command is available, which makes memory map generation faster.
        * In some architectures this may not be possible (e.g. `x86_64`), in which case it will fall back to heuristic detection.
    * It is preferable to run qemu-user on `localhost`.
        * If you run qemu-user on remotely (another host), you can not use the memory patching.

## With Intel Pin
* Usage
    * Listen with `pin -appdebug -appdebug_server_port 1234 -t obj-intel64/inscount0.so -- /PATH/TO/BINARY`.
    * Attach with `gdb-multiarch /PATH/TO/BINARY -ex 'target remote localhost:1234'`.
* Supported architectures
    * Host
        * x64
    * Guest (ELF)
        * x86 and x64
* Note
    * It runs very slowly and is not recommended.

## With Intel SDE
* Usage
    * Listen with `sde64 -debug -debug-port 1234 -- /PATH/TO/BINARY`.
    * Attach with `gdb-multiarch /PATH/TO/BINARY -ex 'target remote localhost:1234'`.
* Supported architectures
    * Host
        * x64
    * Guest (ELF)
        * x86 and x64
* Note
    * It runs very slowly and is not recommended.

## With Qiling framework
* Usage
    * `qltool run -f /PATH/TO/BINARY --rootfs / --gdb :1234`.
        * Or write a harness. See [here](https://docs.qiling.io/en/latest/debugger/).
        * If the architecture is different from the host, specify the appropriate `rootfs` directory.
    * Attach with `gdb-multiarch /PATH/TO/BINARY -ex 'target remote localhost:1234'`.
* Supported architectures
    * Host
        * x64
    * Guest (ELF)
        * x86, x64, ARM and ARM64
* Note
    * On ARM64, the flag register is not available, so the branch taken/not detected is incorrect.
    * This is an experimental support.

## With KGDB
* Usage
    * Host OS
        * Configure 2 `serial port`s as `named pipe` in both (debugger/debuggee) virtual machine settings.
        * Vmware example:
            * Debugger
                * Use named pipe: `\\.\pipe\pipe0` (Windows host) / `/tmp/sock0` (Linux host)
                    * Configure as `This end is the client.` and `The other end is a virtual machine.`
                * Use named pipe: `\\.\pipe\pipe1` (Windows host) / `/tmp/sock1` (Linux host)
                    * configure as `This end is the client.` and `The other end is a virtual machine.`
            * Debuggee
                * Use named pipe: `\\.\pipe\pipe0` (Windows host) / `/tmp/sock0` (Linux Host)
                    * Configure as `This end is the server.` and `The other end is an application.`
                * Use named pipe: `\\.\pipe\pipe1` (Windows host) / `/tmp/sock1` (Linux host)
                    * Configure as `This end is the server.` and `The other end is an application.`
    * Debuggee
        * Build the kernel with configurations such as `CONFIG_KGDB=y`. Ubuntu has supported it by default.
        * Edit `/etc/default/grub` and append `kgdbwait kgdboc=ttyS0,115200 console=ttyS1,115200` to the end of `GRUB_CMDLINE_LINUX_DEFAULT`.
        * Then `update-grub && reboot`.
        * See [official documentation](https://www.kernel.org/doc/html/latest/dev-tools/kgdb.html) for more information.
    * Debugger
        * Attach with `gdb-multiarch -ex 'target remote /dev/ttyS0'`.
        * Connect with `screen /dev/ttyS1` for console.
* Supported architectures
    * Debugger
        * x64
    * Debuggee
        * x64
* Note
    * It needs gdb 12.x or later.
    * It runs very slowly and is not recommended.
    * `Ctrl+C` interrupt does not work. You need to do `echo g > /proc/sysrq-trigger` in console.
    * Many commands are UNSUPPORTED in KGDB mode, because just creating the memory map would take several hours.

## With VMware
* Usage
    * Host OS
        * Add following configurations to vmx file.
            * `debugStub.listen.guest64 = "TRUE"`
            * `debugStub.listen.guest64.remote = "TRUE"`
            * `debugStub.hideBreakpoints = "TRUE"`
            * `debugStub.port.guest64 = "1234"`
            * See [here](https://communities.vmware.com/t5/VMware-Fusion-Discussions/Using-debugStub-to-debug-a-guest-linux-kernel/td-p/394906).
        * Start the guest OS normally.
    * Debugger
        * Attach with `gdb-multiarch -ex 'target remote <ipaddr>:1234'`.
* Supported architectures
    * Debugger
        * x64
    * Debuggee
        * x64
* Note
    * It runs faster than KGDB mode and `Ctrl+C` interrupt works, but it is still slow.
    * Access to physical memory and control registers is possible thanks to the `monitor` command.

## With rr
* Usage
    * Run first, `rr record /PATH/TO/BINARY`.
    * Then, `rr replay` for time-travel debugging.
* Supported architectures
    * Host
        * x64
    * Guest (ELF)
        * x86 and x64
* Note
    * This is an experimental support. Some commands may not work.

## With wine
* Usage
    * Run `winedbg --gdb --no-start /PATH/TO/BINARY` and attach with `gdb -ex 'target remote localhost:<port>'`.
        * If you do not specify the `--no-start` option, gdb will be started directly.
        * However, gdb will be terminated by pressing `Ctrl+C`, so it may be difficult to use.
* Supported architectures
    * Host
       * x64
    * Guest (PE)
       * x86 and x64
* Note
    * It needs to run `winedbg` on `localhost`.
    * This is an experimental support. Some commands may not work.
