# Supported mode

## Standard debugging
- Usage
    - Run `gdb-multiarch` or `gdb` as `root` user.
        - e.g., `gdb-multiarch /PATH/TO/BINARY`, then `run [ARGS]`.
    - Alternatively, `sudo gdb-multiarch /PATH/TO/BINARY`, then `run [ARGS]`.
- Supported architectures
    - Debugger (GDB) host (= Debuggee (ELF) host)
        - x86 and x64
        - Possibly ARM and ARM64
- Notes
    - The following instructions assume that you are the `root` user. Add `sudo` commands as needed.
    - The instructions also assume that you use `gdb-multiarch`. Of course, you can use `gdb`.

## Attaching to a running process
- Usage
    - Run `gdb-multiarch /PATH/TO/BINARY -p PID`.
- Supported architectures
    - Debugger (GDB) host (= Debuggee (ELF) host)
        - x86 and x64
        - Possibly ARM and ARM64

## With Docker
- Usage
    - Attach from outside of Docker using `gdb-multiarch /PATH/TO/BINARY -p PID`.
        - The `PID` refers to the process ID visible to the host.
- Supported architectures
    - Debugger (GDB) host (= Debuggee (Docker, ELF) host)
        - x86 and x64
        - Possibly ARM and ARM64
- Notes
    - You can also install and use GEF inside Docker.
    - However, the `--privileged` option is required when running `docker run` or `docker exec`.

## With Gdbserver
- Usage
    - Start `gdbserver localhost:1234 /PATH/TO/BINARY [ARGS]` to listen on port `0.0.0.0:1234`.
    - Attach using `gdb-multiarch -ex 'target remote <IP address>:1234'`.
- Supported architectures
    - Debugger (GDB) host
        - x86 and x64
        - Possibly ARM and ARM64
    - Debugger stub (Gdbserver) host (= Debuggee (ELF) host)
        - x86 and x64
        - Possibly ARM and ARM64

## With Qemu-system
- Usage
    - Start `qemu-system` with the `-s` option to listen on `localhost:1234`.
        - If you want to change the listening port, use the `-gdb tcp::9876` option.
    - Attach using `gdb-multiarch -ex 'target remote localhost:1234'`.
        - Alternatively, use `gdb-multiarch -ex 'set architecture TARGET_ARCH' -ex 'target remote localhost:1234'` (for old versions of QEMU).
- Supported architectures
    - Debugger (GDB) host
        - x64
    - Debugger stub (Qemu-system) host
        - x64
    - Debuggee (Qemu-system guest)
        - x86, x64, ARM and ARM64
        - i8086 (16-bit) is supported experimentally.
- Notes
    - Most commands should work fine unless `CONFIG_RANDSTRUCT=y`.
    - It works with any version of `qemu-system`, but the latest version is recommended.
    - It is preferable to run `qemu-system` on `localhost`.
        - If you run `qemu-system` remotely (another host), you can not handle SecureWorld's memory.
    - For more information, see [docs/FAQ.md](FAQ.md).

## With Qemu-user
- Usage
    - Start `qemu-user` with the `-g 1234` option to listen on `localhost:1234`.
    - Attach using `gdb-multiarch /PATH/TO/BINARY -ex 'target remote localhost:1234'`.
        - Alternatively, use `gdb-multiarch -ex 'set architecture TARGET_ARCH' -ex 'target remote localhost:1234'` (for old versions of QEMU).
- Supported architectures
    - Debugger (GDB) host
        - x64
    - Debugger stub (Qemu-user) host
        - x64
    - Debuggee (ELF)
        - See [docs/QEMU-USER-SUPPORTED-ARCH.md](QEMU-USER-SUPPORTED-ARCH.md) for details.
- Notes
    - It works with any version of `qemu-user`, but the latest version is recommended.
        - From QEMU 8.1 onwards, the `info proc mappings` command is supported in `qemu-user`, which significantly speeds up memory map generation.
        - However, in some architectures (e.g., `x86_64`), this may not be possible, and it will fall back to heuristic detection.
    - It is preferable to run `qemu-user` on `localhost`.
        - If you run `qemu-user` remotely (another host), you can not use memory patching.

## With Intel Pin
- Usage
    - Listen using `pin -appdebug -appdebug_server_port 1234 -t obj-intel64/inscount0.so -- /PATH/TO/BINARY`.
    - Attach using `gdb-multiarch /PATH/TO/BINARY -ex 'target remote localhost:1234'`.
- Supported architectures
    - Debugger (GDB) host
        - x64
    - Debugger stub (Intel Pin) host
        - x64
    - Debuggee (ELF)
        - x86 and x64
- Note
    - This runs very slowly and is not recommended.

## With Intel SDE
- Usage
    - Listen using `sde64 -debug -debug-port 1234 -- /PATH/TO/BINARY`.
    - Attach using `gdb-multiarch /PATH/TO/BINARY -ex 'target remote localhost:1234'`.
- Supported architectures
    - Debugger (GDB) host
        - x64
    - Debugger stub (Intel SDE) host
        - x64
    - Debuggee (ELF)
        - x86 and x64
- Note
    - This runs very slowly and is not recommended.

## With Qiling framework
- Usage
    - Run `qltool run -f /PATH/TO/BINARY --rootfs / --gdb :1234`.
        - Alternatively, write a harness. See [here](https://docs.qiling.io/en/latest/debugger/) for more information.
        - If the target architecture differs from the host architecture, specify the appropriate `rootfs` directory.
    - Attach using `gdb-multiarch /PATH/TO/BINARY -ex 'target remote localhost:1234'`.
- Supported architectures
    - Debugger (GDB) host
        - x64
    - Debugger stub (Qiling framework) host
        - x64
    - Debuggee (ELF)
        - x86, x64, ARM and ARM64
- Notes
    - When debugging ARM64 binaries, the flag register is not available, so branch taken/not taken detection may be incorrect.
    - This is experimental support, so some commands may not work.

## With KGDB
- Usage
    - Host OS
        - Configure two serial ports as named pipes in both the debugger and debuggee virtual machine settings.
        - Vmware example:
            - Debugger
                - Use named pipe: `\\.\pipe\pipe0` (Windows host) / `/tmp/sock0` (Linux host)
                    - Configure as `This end is the client.` and `The other end is a virtual machine.`
                - Use named pipe: `\\.\pipe\pipe1` (Windows host) / `/tmp/sock1` (Linux host)
                    - configure as `This end is the client.` and `The other end is a virtual machine.`
            - Debuggee
                - Use named pipe: `\\.\pipe\pipe0` (Windows host) / `/tmp/sock0` (Linux Host)
                    - Configure as `This end is the server.` and `The other end is an application.`
                - Use named pipe: `\\.\pipe\pipe1` (Windows host) / `/tmp/sock1` (Linux host)
                    - Configure as `This end is the server.` and `The other end is an application.`
    - Debuggee
        - Build the kernel with configurations such as `CONFIG_KGDB=y`. Ubuntu supports this by default.
        - Edit `/etc/default/grub` and append `kgdbwait kgdboc=ttyS0,115200 console=ttyS1,115200` to the end of `GRUB_CMDLINE_LINUX_DEFAULT`.
        - Then run `update-grub && reboot`.
        - See [official documentation](https://www.kernel.org/doc/html/latest/dev-tools/kgdb.html) for more information.
    - Debugger
        - Attach using `gdb-multiarch -ex 'target remote /dev/ttyS0'`.
        - Connect with `screen /dev/ttyS1` for console access.
- Supported architectures
    - Debugger (GDB) host
        - x64
    - Debuggee (debugged kernel)
        - x64
- Notes
    - You need `gdb` version 12.x or later.
    - This runs very slowly and is not recommended.
    - The `Ctrl+C` interrupt does not work; instead, use `echo g > /proc/sysrq-trigger` in the console.
    - Many commands are unsupported in KGDB mode because creating the memory map would take several hours.

## With VMware
- Usage
    - Host OS
        - Add the following configurations to the `vmx` file.
            - `debugStub.listen.guest64 = "TRUE"`
            - `debugStub.listen.guest64.remote = "TRUE"`
            - `debugStub.hideBreakpoints = "TRUE"`
            - `debugStub.port.guest64 = "1234"`
            - See [here](https://communities.vmware.com/t5/VMware-Fusion-Discussions/Using-debugStub-to-debug-a-guest-linux-kernel/td-p/394906).
        - Start the guest OS normally.
    - Debugger
        - Attach using `gdb-multiarch -ex 'target remote <IP address>:1234'`.
- Supported architectures
    - Debugger (GDB) host
        - x64
    - Debuggee (debugged kernel)
        - x64
- Notes
    - It runs faster than KGDB mode, and `Ctrl+C` interrupt works, but it is still slow.
    - Access to physical memory and control registers is possible thanks to the `monitor` command.

## With rr
- Usage
    - First, run `rr record /PATH/TO/BINARY`.
    - Then, use `rr replay` for time-travel debugging.
- Supported architectures
    - Debugger (`rr`) host (= Debuggee (ELF) host)
        - x86 and x64
- Note
    - This is experimental support, so some commands may not work.

## With Wine
- Usage
    - Run `winedbg --gdb --no-start /PATH/TO/BINARY` and attach using `gdb -ex 'target remote localhost:<port>'`.
        - It is recommended to use the `--no-start` option because pressing `Ctrl+C` without `--no-start` will terminate `gdb`.
- Supported architectures
    - Debugger (GDB) host
        - x64
    - Debugger stub (`winedbg`) host
        - x64
    - Debuggee (PE)
        - x86 and x64
- Notes
    - You must run `winedbg` on `localhost`.
    - This is experimental support, so some commands may not work.

## With Qemu-system for Android kernel (when using Android Studio)
- Usage
    - Start as `emulator -avd <AVD_NAME> -no-audio -no-snapshot -qemu -s` to listen on `localhost:1234`.
        - If `-no-audio -no-snapshot` are not necessary, you can remove them.
        - Available `<AVD_NAME>` values can be obtained with `emulator -list-avds`.
    - Attach using `gdb-multiarch -ex 'set architecture i386:x86-64' -ex 'target remote localhost:1234'`.
- Supported architectures
    - Debugger (GDB) host
        - x64
    - Debugger stub (Qemu-system) host
        - x64
    - Debuggee (Qemu-system guest)
        - x64
        - Possibly x86, ARM and ARM64
- Notes
    - This method sometimes fails.
        - For more information, see [docs/FAQ.md](FAQ.md).
        - If an issue occurs, try closing `gdb` and reconnecting.
    - To connect from another machine, specify the IP address.
        - `gdb-multiarch -ex 'set architecture i386:x86-64' -ex 'target remote <Android Studio host machine's IP address>:1234'`.

## With Android userland binary (when using Android Studio)
- Usage
    - Setup `adb` settings.
        - Run `adb root` if necessary.
        - Use `adb forward tcp:9999 tcp:9999` for port forwarding.
    - Push the statically built `gdbserver` to the Android device.
        - `adb push gdbserver-static /data/local/tmp`.
        - `adb shell chmod +x /data/local/tmp/gdbserver-static`.
    - Start `gdbserver`.
        - `adb shell /data/local/tmp/gdbserver-static localhost:9999 /PATH/TO/BINARY`.
    - Attach using `gdb-multiarch 'target remote localhost:9999'`.
- Supported architectures
    - Debugger (GDB) host
        - x64
    - Debugger stub (Gdbserver) host (= Debuggee (ELF) host)
        - x64
        - Possibly x86, ARM and ARM64
- Notes
    - To connect from another machine, you can forward the port further.
        - Run `socat TCP-LISTEN:9998,fork,reuseaddr TCP-CONNECT:localhost:9999` on the `Android Studio` host machine.
        - Attach using `gdb-multiarch 'target remote <Android Studio host machine's IP address>:9998'` from another machine.
