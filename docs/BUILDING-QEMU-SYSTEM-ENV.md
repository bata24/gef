## Building Qemu

```bash
apt install libslirp-dev
apt build-dep qemu ninja-build

wget https://download.qemu.org/qemu-9.2.0.tar.xz
tar xf qemu-9.2.0.tar.xz
cd qemu-9.2.0
cp -r pc-bios /usr/local/bin

./configure --enable-slirp
make -j
make install
```

## buildroot x86-64
```bash
tar xf buildroot-2024.11.1.tar.xz
cd buildroot-2024.11.1/
make qemu_x86_64_defconfig
make

qemu-system-x86_64 \
    -M pc \
    -m 512M \
    -cpu kvm64,+smep,+smap \
    -kernel output/images/bzImage \
    -drive file=output/images/rootfs.ext2,if=virtio,format=raw \
    -append "rootwait root=/dev/vda console=tty1 console=ttyS0 noapic" \
    -net nic,model=virtio \
    -net user \
    -nographic \
    -monitor telnet:127.0.0.1:9999,server,nowait \
    -s
```

- Notes
    - Various default build configs for buildroot are in `configs/`.
        - When you run `make qemu_x86_64_defconfig`, it will be copied to `.config` in the top directory and used.
    - The build configuration for the Linux kernel is in `board/qemu/*/linux.config`.
        - Change this if you want to change the configuration.
        - Or copy it to another location and specify the following in the build configuration (`.config`) of buildroot itself in the top directory.
            - `BR2_LINUX_KERNEL_USE_CUSTOM_CONFIG=y`
            - `BR2_LINUX_KERNEL_CUSTOM_CONFIG_FILE="/path/to/config"`
    - The startup command is written in `board/qemu/*/readme.txt`.
        - Modify it as appropriate, for example adding `-nographic` or removing `-serial`.
    - If the Qemu download is too slow, abort the build, switch to the mirror site as follows, and make again.
        ```
        vi package/qemu/qemu.mk
        -QEMU_SITE = http://download.qemu.org
        +QEMU_SITE = https://mirror.koddos.net/blfs/conglomeration/qemu
        ```
    - If you want to replace the kernel with the latest version, just build the kernel, replace the `bzImage`, and start it.
        ```
        git clone https://github.com/torvalds/linux.git
        cd linux/
        make defconfig
        make

        # If you want to cross compile here,
        #     For i386: make defconfig && make ARCH=i386
        #     For AArch64: make ARCH=arm64 defconfig && make ARCH=arm64 CROSS_COMPILE="aarch64-linux-gnu-"
        #     For ARM: make ARCH=arm defconfig && make ARCH=arm CROSS_COMPILE="arm-linux-gnueabihf-"

        qemu-system-x86_64 \
            -M pc \
            -kernel kernel/linux/arch/x86_64/boot/bzImage \
            -drive file=buildroot-2024.11.1/output/images/rootfs.ext2,if=ide \
            -append "root=/dev/sda console=ttyS0" \
            -nographic \
            -netdev tap,id=tap0 \
            -device e1000,netdev=tap0 \
            -monitor telnet:127.0.0.1:9999,server,nowait \
            -s

        # Note 1
        # When I updated the kernel, eth0 was no longer recognized for some reason,
        # so I recommend creating tap0 with the qemu command (-netdev tap,id=tap0 -device e1000,netdev=tap0) and attaching it.
        # https://unix.stackexchange.com/questions/171874/no-network-interface-in-qemu

        # Note 2
        # For some reason, the new kernel no longer recognizes /dev/vda,
        # so it is a good idea to change the type to ide and start it as /dev/sda
        # (virtio: /dev/vda, ide connection: /dev/sda, SD card: /dev/mmcblk0).
        ```

## buildroot x86
```bash
tar xf buildroot-2024.11.1.tar.xz
cd buildroot-2024.11.1/
make qemu_x86_defconfig
make

qemu-system-i386 \
    -M pc \
    -kernel output/images/bzImage \
    -drive file=output/images/rootfs.ext2,if=virtio,format=raw \
    -append "rootwait root=/dev/vda console=tty1 console=ttyS0" \
    -net nic,model=virtio \
    -net user \
    -nographic \
    -monitor telnet:127.0.0.1:9999,server,nowait \
    -s
```

## buildroot ARM
```bash
tar xf buildroot-2024.11.1.tar.xz
cd buildroot-2024.11.1/
make qemu_arm_vexpress_defconfig
make

qemu-system-arm \
    -M vexpress-a9 \
    -m 256 \
    -kernel output/images/zImage \
    -dtb output/images/vexpress-v2p-ca9.dtb \
    -drive file=output/images/rootfs.ext2,if=sd,format=raw \
    -append "console=ttyAMA0,115200 rootwait root=/dev/mmcblk0" \
    -net nic,model=lan9118 \
    -net user \
    -nographic \
    -monitor telnet:127.0.0.1:9999,server,nowait \
    -s
```

- Notes
    - In the case of ARM (vexpress), there is no configuration in `board/qemu/arm-vexpress/linux.config`.
    - The following steps are necessary (I think), but I'm not sure what the correct way is.
        - Build once with buildroot
        - Copy the generated `output/build/linux-XXX/.config` to another location and modify the contents
        - Specify `.config` with `BR2_LINUX_KERNEL_CUSTOM_CONFIG_FILE`.

## buildroot AArch64
```bash
tar xf buildroot-2024.11.1.tar.xz
cd buildroot-2024.11.1/
make qemu_aarch64_virt_defconfig
make

qemu-system-aarch64 \
    -M virt \
    -cpu cortex-a53 \
    -smp 1 \
    -kernel output/images/Image \
    -append "rootwait root=/dev/vda console=ttyAMA0" \
    -netdev user,id=eth0 \
    -device virtio-net-device,netdev=eth0 \
    -drive file=output/images/rootfs.ext4,if=none,format=raw,id=hd0 \
    -device virtio-blk-device,drive=hd0 \
    -nographic \
    -monitor telnet:127.0.0.1:9999,server,nowait \
    -s
```

## buildroot mipsel
```bash
tar xf buildroot-2024.11.1.tar.xz
cd buildroot-2024.11.1/
make qemu_mips32r6el_malta_defconfig
make

qemu-system-mipsel \
    -M malta \
    -cpu mips32r6-generic \
    -kernel output/images/vmlinux \
    -drive file=output/images/rootfs.ext2,format=raw \
    -append "rootwait root=/dev/hda" \
    -net nic,model=pcnet \
    -net user \
    -nographic \
    -monitor telnet:127.0.0.1:9999,server,nowait \
    -s
```

## buildroot mips
```bash
tar xf buildroot-2024.11.1.tar.xz
cd buildroot-2024.11.1/
make qemu_mips32r6_malta_defconfig
make

qemu-system-mips \
    -M malta \
    -cpu mips32r6-generic \
    -kernel output/images/vmlinux \
    -drive file=output/images/rootfs.ext2,format=raw \
    -append "rootwait root=/dev/hda" \
    -net nic,model=pcnet \
    -net user \
    -nographic \
    -monitor telnet:127.0.0.1:9999,server,nowait \
    -s
```

## buildroot mips64el
```bash
tar xf buildroot-2024.11.1.tar.xz
cd buildroot-2024.11.1/
make qemu_mips64r6el_malta_defconfig
make

qemu-system-mips64el \
    -M malta \
    -cpu I6400 \
    -kernel output/images/vmlinux \
    -drive file=output/images/rootfs.ext2,format=raw \
    -append "rootwait root=/dev/hda" \
    -nographic \
    -monitor telnet:127.0.0.1:9999,server,nowait \
    -s
```

## buildroot mips64
```bash
tar xf buildroot-2024.11.1.tar.xz
cd buildroot-2024.11.1/
make qemu_mips64r6_malta_defconfig
make

qemu-system-mips64el \
    -M malta \
    -cpu I6400 \
    -kernel output/images/vmlinux \
    -drive file=output/images/rootfs.ext2,format=raw \
    -append "rootwait root=/dev/hda" \
    -nographic \
    -monitor telnet:127.0.0.1:9999,server,nowait \
    -s
```

## debian x86-64
```bash
wget https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-12.9.0-amd64-netinst.iso
qemu-img create -f qcow2 disk.qcow2 20G

# For some reason, adding -nographic -serial mon:stdio did not work as the output was not displayed on the screen,
# so I started it without those options and set it up in a GUI environment.
qemu-system-x86_64 \
    -enable-kvm \
    -m 2G \
    -hda disk.qcow2 \
    -net nic,model=virtio \
    -net user \
    -cdrom debian-12.9.0-amd64-netinst.iso \
    -boot d

# Open disk.qcow2 with 7-zip file manager and extract the following two files:
0.img/boot/initrd.img-6.1.123-amd64
0.img/boot/vmlinuz-6.1.123-amd64

# Run
qemu-system-x86_64 \
    -enable-kvm \
    -m 2G \
    -hda disk.qcow2 \
    -kernel vmlinuz-6.1.123-1-amd64 \
    -append 'root=/dev/sda1 console=ttyS0' \
    -initrd initrd.img-6.1.123-1-amd64 \
    -net nic,model=virtio \
    -net user,hostfwd=tcp:127.0.0.1:2222-:22 \
    -nographic \
    -serial mon:stdio \
    -s
```

## debian x86
```bash
wget https://cdimage.debian.org/debian-cd/current/i386/iso-cd/debian-12.9.0-i386-netinst.iso
qemu-img create -f qcow2 disk.qcow2 20G

# For some reason, adding -nographic -serial mon:stdio did not work as the output was not displayed on the screen,
# so I started it without those options and set it up in a GUI environment.
qemu-system-i386 \
    -enable-kvm \
    -m 2G \
    -hda disk.qcow2 \
    -net nic,model=virtio \
    -net user \
    -cdrom debian-12.9.0-i386-netinst.iso \
    -boot d

# Open disk.qcow2 with 7-zip file manager and extract the following two files:
0.img/boot/initrd.img-6.1.123-1-686-pae
0.img/boot/vmlinuz-6.1.123-1-686-pae

# Run
qemu-system-i386 \
    -enable-kvm \
    -m 2G \
    -hda disk.qcow2 \
    -kernel vmlinuz-6.1.123-1-686-pae \
    -append 'root=/dev/sda1 console=ttyS0' \
    -initrd initrd.img-6.1.123-1-686-pae \
    -net nic,model=virtio \
    -net user,hostfwd=tcp:127.0.0.1:2222-:22 \
    -nographic \
    -serial mon:stdio \
    -s
```

## debian ARM
```bash
wget http://ftp.debian.org/debian/dists/Debian10.4/main/installer-armhf/current/images/netboot/initrd.gz
wget http://ftp.debian.org/debian/dists/Debian10.4/main/installer-armhf/current/images/netboot/vmlinuz
qemu-img create -f qcow2 disk.qcow2 20G

# Select C for language and your country (e.g. Japan or Japanese, etc.) for others.
# Please note that mirror download destinations may not work properly in some cases.
# Installation takes about 2 hours.
# You may get a grub installation error, but you can ignore it and proceed.
# When it's time for the final reboot, use pkill -9 qemu from another terminal to force it to terminate.
qemu-system-arm \
    -smp 2 \
    -M virt \
    -cpu cortex-a15 \
    -m 1G \
    -initrd initrd.gz \
    -kernel vmlinuz \
    -append "root=/dev/ram console=ttyAMA0" \
    -global virtio-blk-device.scsi=off \
    -device virtio-scsi-device,id=scsi \
    -drive file=disk.qcow2,id=rootimg,cache=unsafe,if=none \
    -device scsi-hd,drive=rootimg \
    -netdev user,id=unet \
    -device virtio-net-device,netdev=unet \
    -net user \
    -nographic \
    -s

# Copy kernel and ramdisk
apt install nbd-client && modprobe nbd max_part=8 && qemu-nbd --connect=/dev/nbd0 disk.qcow2
mkdir mnt && mount /dev/nbd0p1 mnt && cp mnt/initrd.img-*-armmp-lpae mnt/vmlinuz-*-armmp-lpae . && sync
umount /dev/nbd0p1 && nbd-client -d /dev/nbd0 && rmdir mnt && rm -f initrd.gz vmlinuz

# Run
qemu-system-arm \
    -smp 2 \
    -M virt \
    -cpu cortex-a15 \
    -m 1G \
    -initrd initrd.img-4.19.0-9-armmp-lpae \
    -kernel vmlinuz-4.19.0-9-armmp-lpae \
    -append "root=/dev/sda2 console=ttyAMA0" \
    -global virtio-blk-device.scsi=off \
    -device virtio-scsi-device,id=scsi \
    -drive file=disk.qcow2,id=rootimg,cache=unsafe,if=none \
    -device scsi-hd,drive=rootimg \
    -device virtio-net-device,netdev=net0 \
    -netdev user,hostfwd=tcp:127.0.0.1:2222-:22,id=net0 \
    -nographic \
    -s
```

## debian AArch64
```bash
wget http://ftp.debian.org/debian/dists/Debian10.4/main/installer-arm64/current/images/netboot/debian-installer/arm64/initrd.gz
wget http://ftp.debian.org/debian/dists/Debian10.4/main/installer-arm64/current/images/netboot/debian-installer/arm64/linux
qemu-img create -f qcow2 disk.qcow2 20G

# Select C for language and your country (e.g. Japan or Japanese, etc.) for others.
# Please note that mirror download destinations may not work properly in some cases.
# Installation takes about 2 hours.
# You may get a grub installation error, but you can ignore it and proceed.
# When it's time for the final reboot, use pkill -9 qemu from another terminal to force it to terminate.
qemu-system-aarch64 \
    -smp 2 \
    -M virt \
    -cpu cortex-a57 \
    -m 1G \
    -initrd initrd.gz \
    -kernel linux \
    -append "root=/dev/ram console=ttyAMA0" \
    -global virtio-blk-device.scsi=off \
    -device virtio-scsi-device,id=scsi \
    -drive file=disk.qcow2,id=rootimg,cache=unsafe,if=none \
    -device scsi-hd,drive=rootimg \
    -netdev user,id=unet \
    -device virtio-net-device,netdev=unet \
    -net user \
    -nographic \
    -s

# Copy kernel and ramdisk
apt install nbd-client && modprobe nbd max_part=8 && qemu-nbd --connect=/dev/nbd0 disk.qcow2
mkdir mnt && mount /dev/nbd0p1 mnt && cp mnt/initrd.img-*-arm64 mnt/vmlinuz-*-arm64 . && sync
umount /dev/nbd0p1 && nbd-client -d /dev/nbd0 && rmdir mnt && rm -f initrd.gz linux

# Run
qemu-system-aarch64
    -smp 2 \
    -M virt \
    -cpu cortex-a57 \
    -m 1G \
    -initrd initrd.img-4.19.0-9-arm64 \
    -kernel vmlinuz-4.19.0-9-arm64 \
    -append "root=/dev/sda2 console=ttyAMA0" \
    -global virtio-blk-device.scsi=off \
    -device virtio-scsi-device,id=scsi \
    -drive file=disk.qcow2,id=rootimg,cache=unsafe,if=none \
    -device scsi-hd,drive=rootimg \
    -device virtio-net-device,netdev=net0 \
    -netdev user,hostfwd=tcp:127.0.0.1:2222-:22,id=net0 \
    -nographic \
    -s
```

## debian mipsel
```bash
wget http://ftp.debian.org/debian/dists/Debian10.4/main/installer-mipsel/current/images/malta/netboot/initrd.gz
wget http://ftp.debian.org/debian/dists/Debian10.4/main/installer-mipsel/current/images/malta/netboot/vmlinux-4.19.0-9-4kc-malta
qemu-img create -f qcow2 disk.qcow2 20G

# Select C for language and your country (e.g. Japan or Japanese, etc.) for others.
# Please note that mirror download destinations may not work properly in some cases.
# Installation takes about 2 hours.
# You may get a grub installation error, but you can ignore it and proceed.
# When it's time for the final reboot, use pkill -9 qemu from another terminal to force it to terminate.
qemu-system-mipsel \
    -M malta \
    -m 1G \
    -hda ./disk.qcow2 \
    -initrd ./initrd.gz \
    -kernel ./vmlinux-4.19.0-9-4kc-malta \
    -append "nokaslr" \
    -nographic

# Copy kernel and ramdisk
apt install nbd-client && modprobe nbd max_part=8 && qemu-nbd --connect=/dev/nbd0 disk.qcow2
mkdir mnt && mount /dev/nbd0p1 mnt && cp mnt/boot/initrd.img-*-malta . && sync
umount /dev/nbd0p1 && nbd-client -d /dev/nbd0 && rmdir mnt && rm -f initrd.gz

# Run
qemu-system-mipsel \
    -M malta \
    -m 1G \
    -hda ./disk.qcow2 \
    -initrd ./initrd.img-4.19.0-9-4kc-malta \
    -kernel ./vmlinux-4.19.0-9-4kc-malta \
    -append "nokaslr root=/dev/sda1" \
    -net nic,model=e1000 \
    -net user,hostfwd=tcp:127.0.0.1:2222-:22,id=net0 \
    -nographic
```

```bash
# Execute in the guest

# fix interface
cat > /etc/network/interfaces << EOF
auto lo
auto enp0s18
iface lo inet loopback
iface enp0s18 inet dhcp
EOF
systemctl restart networking
```

## debian mips
```bash
wget http://ftp.debian.org/debian/dists/Debian10.4/main/installer-mips/current/images/malta/netboot/initrd.gz
wget http://ftp.debian.org/debian/dists/Debian10.4/main/installer-mips/current/images/malta/netboot/vmlinux-4.19.0-9-4kc-malta
qemu-img create -f qcow2 disk.qcow2 20G

# Select C for language and your country (e.g. Japan or Japanese, etc.) for others.
# Please note that mirror download destinations may not work properly in some cases.
# Installation takes about 2 hours.
# You may get a grub installation error, but you can ignore it and proceed.
# When it's time for the final reboot, use pkill -9 qemu from another terminal to force it to terminate.
qemu-system-mips \
    -M malta \
    -m 1G \
    -hda ./disk.qcow2 \
    -initrd ./initrd.gz \
    -kernel ./vmlinux-4.19.0-9-4kc-malta \
    -append "nokaslr" \
    -nographic

# Copy kernel and ramdisk
apt install nbd-client && modprobe nbd max_part=8 && qemu-nbd --connect=/dev/nbd0 disk.qcow2
mkdir mnt && mount /dev/nbd0p1 mnt && cp mnt/boot/initrd.img-*-malta . && sync
umount /dev/nbd0p1 && nbd-client -d /dev/nbd0 && rmdir mnt && rm -f initrd.gz

# Run
qemu-system-mips \
    -M malta \
    -m 1G \
    -hda ./disk.qcow2 \
    -initrd ./initrd.img-4.19.0-9-4kc-malta \
    -kernel ./vmlinux-4.19.0-9-4kc-malta \
    -append "nokaslr root=/dev/sda1" \
    -net nic,model=e1000 \
    -net user,hostfwd=tcp:127.0.0.1:2222-:22,id=net0 \
    -nographic
```

```bash
# Execute in the guest

# fix interface
cat > /etc/network/interfaces << EOF
auto lo
auto enp0s18
iface lo inet loopback
iface enp0s18 inet dhcp
EOF
systemctl restart networking
```

## debian mips64el
```bash
wget http://ftp.debian.org/debian/dists/Debian10.4/main/installer-mips64el/current/images/malta/netboot/initrd.gz
wget http://ftp.debian.org/debian/dists/Debian10.4/main/installer-mips64el/current/images/malta/netboot/vmlinux-4.19.0-9-5kc-malta
qemu-img create -f qcow2 disk.qcow2 20G

# Select C for language and your country (e.g. Japan or Japanese, etc.) for others.
# Please note that mirror download destinations may not work properly in some cases.
# Installation takes about 2 hours.
# You may get a grub installation error, but you can ignore it and proceed.
# When it's time for the final reboot, use pkill -9 qemu from another terminal to force it to terminate.
qemu-system-mips64el \
    -M malta \
    -cpu MIPS64R2-generic \
    -m 1G \
    -hda ./disk.qcow2 \
    -initrd ./initrd.gz \
    -kernel ./vmlinux-4.19.0-9-5kc-malta \
    -append "nokaslr" \
    -nographic

# Copy kernel and ramdisk
apt install nbd-client && modprobe nbd max_part=8 && qemu-nbd --connect=/dev/nbd0 disk.qcow2
mkdir mnt && mount /dev/nbd0p1 mnt && cp mnt/boot/initrd.img-*-malta . && sync
umount /dev/nbd0p1 && nbd-client -d /dev/nbd0 && rmdir mnt && rm -f initrd.gz

# Run
qemu-system-mips64el \
    -M malta \
    -cpu MIPS64R2-generic \
    -m 1G \
    -hda ./disk.qcow2 \
    -initrd ./initrd.img-4.19.0-9-5kc-malta \
    -kernel ./vmlinux-4.19.0-9-5kc-malta \
    -append "nokaslr root=/dev/sda1" \
    -net nic,model=e1000 \
    -net user,hostfwd=tcp:127.0.0.1:2222-:22,id=net0 \
    -nographic
```

```bash
# Execute in the guest

# fix interface
cat > /etc/network/interfaces << EOF
auto lo
auto enp0s18
iface lo inet loopback
iface enp0s18 inet dhcp
EOF
systemctl restart networking
```

## debian ppc64el
```bash
wget http://ftp.debian.org/debian/dists/Debian10.4/main/installer-ppc64el/current/images/netboot/debian-installer/ppc64el/initrd.gz
wget http://ftp.debian.org/debian/dists/Debian10.4/main/installer-ppc64el/current/images/netboot/debian-installer/ppc64el/vmlinux
qemu-img create -f qcow2 disk.qcow2 20G

# Select C for language and your country (e.g. Japan or Japanese, etc.) for others.
# Please note that mirror download destinations may not work properly in some cases.
# Installation takes about 2 hours.
# You may get a grub installation error, but you can ignore it and proceed.
# When it's time for the final reboot, use pkill -9 qemu from another terminal to force it to terminate.
qemu-system-ppc64 \
    -M pseries-2.12 \
    -cpu power9 \
    -smp 2 \
    -m 2G \
    -hda disk.qcow2 \
    -initrd ./initrd.gz \
    -kernel ./vmlinux \
    -append "nokaslr" \
    -net nic,macaddr=52:54:00:fa:ce:12,model=virtio \
    -net user \
    -nographic \
    -nodefaults \
    -serial stdio

# Open disk.qcow2 with 7-zip file manager and extract the following two files:
1.img/boot/initrd.img-4.19.0-9-powerpc64le
1.img/boot/vmlinux-4.19.0-9-powerpc64le

# Delete the kernel and ramdisk used during installation
rm -f initrd.gz vmlinux

# Run
qemu-system-ppc64 \
    -M pseries-2.12 \
    -cpu power9 \
    -smp 2 \
    -m 2G \
    -hda disk.qcow2 \
    -initrd ./initrd.img-4.19.0-9-powerpc64le \
    -kernel ./vmlinux-4.19.0-9-powerpc64le \
    -append "nokaslr root=/dev/sda2" \
    -net nic,macaddr=52:54:00:fa:ce:12,model=virtio \
    -net user,hostfwd=tcp:127.0.0.1:2222-:22,id=net0 \
    -nographic \
    -nodefaults \
    -serial stdio
```

## debian sparc64
```bash
# Versions later than 9.0 will not install properly.
wget http://cdimage.debian.org/cdimage/ports/9.0/sparc64/iso-cd/debian-9.0-sparc64-NETINST-1.iso
qemu-img create -f qcow2 disk.qcow2 20G

# Press Enter to start booting from the CD, select C for language and your country (e.g. Japan or Japanese, etc.) for others.
# You will be told that there is no NIC, but this is what you intended so select "no ethernet card" and proceed.
# When asked whether to scan another CD/DVD, select No and proceed.
# When it comes to entering the mirror, press "Go Back" to skip the installation from the network and proceed.
# Installation takes about 2 hours.
# You may get a grub installation error, but you can ignore it and proceed.
# When it's time for the final reboot, use pkill -9 qemu from another terminal to force it to terminate.
qemu-system-sparc64 \
    -m 2G \
    -hda disk.qcow2 \
    -cdrom debian-9.0-sparc64-NETINST-1.iso \
    -boot once=d \
    -serial stdio \
    -nographic \
    -nodefaults

# Run
qemu-system-sparc64 \
    -machine sun4u,accel=tcg,usb=off \
    -m 2G \
    -realtime mlock=off \
    -smp 1,sockets=1,cores=1,threads=1 \
    -uuid ccd8b5c2-b8e4-4d5e-af19-9322cd8e55bf \
    -rtc base=utc \
    -no-reboot \
    -no-shutdown \
    -boot strict=on \
    -drive file=disk.qcow2,if=none,id=hd,format=qcow2,cache=none,aio=native \
    -device ide-hd,bus=ide.0,unit=0,drive=hd \
    -net nic,model=e1000 \
    -net user,hostfwd=tcp:127.0.0.1:2222-:22,id=net0 \
    -msg timestamp=on \
    -serial mon:stdio \
    -nographic \
    -nodefaults
```

```bash
# Execute in the guest

# fix interface
cat > /etc/network/interfaces << EOF
auto lo
auto enp2s0
iface lo inet loopback
iface enp2s0 inet dhcp
EOF
systemctl restart networking

# Added blacklist module
cat > /etc/modprobe.d/drm-blacklist.conf << EOF
# blacklist of DRM modules that do not load on qemu-system-sparc64 sun4u
blacklist drm
blacklist bochs-drm
blacklist ttm
EOF

# Add the apt repository and key that are missing.
echo 'deb http://ftp.ports.debian.org/debian-ports/ unstable main' > /etc/apt/sources.list
busybox wget http://ftp.ports.debian.org/debian-ports/pool/main/d/debian-ports-archive-keyring/debian-ports-archive-keyring_2019.11.05_all.deb
dpkg -i debian-ports-archive-keyring_2019.11.05_all.deb && rm debian-ports-archive-keyring_2019.11.05_all.deb

# Parallel disk writing occurs during apt, causing frequent I/O errors.
# As a countermeasure, save the apt cache to tmpfs.
# Of course, this will disappear when you restart the computer.
mv /var/cache/apt/archives/* /tmp
rmdir /var/cache/apt/archives
ln -s /tmp /var/cache/apt/archives
```

## debian s390x
```bash
wget https://cdimage.debian.org/pub/debian/dists/stretch/main/installer-s390x/current/images/generic/kernel.debian
wget https://cdimage.debian.org/pub/debian/dists/stretch/main/installer-s390x/current/images/generic/initrd.debian
qemu-img create -f qcow2 disk.qcow2 20G

# You will first be asked for the NIC and IP, so enter the model as virtio, IP as 10.0.2.15, default as 10.0.2.2, and DNS as 10.0.2.3.
# Select C for language and your country (e.g. Japan or Japanese, etc.) for others.
# Please note that mirror download destinations may not work properly in some cases.
# Installation takes about 2 hours.
# You may get a grub installation error, but you can ignore it and proceed.
# When it's time for the final reboot, use pkill -9 qemu from another terminal to force it to terminate.
qemu-system-s390x \
    -M s390-ccw-virtio \
    -m 2G \
    -kernel kernel.debian \
    -initrd initrd.debian \
    -drive file=disk.qcow2,if=none,format=qcow2,id=hd0 \
    -device virtio-blk-ccw,drive=hd0,id=virtio-disk0 \
    -net nic,macaddr=52:54:00:fa:ce:18,model=virtio \
    -net user \
    -nographic

# Copy kernel and ramdisk
apt install nbd-client && modprobe nbd max_part=8 && qemu-nbd --connect=/dev/nbd0 disk.qcow2
mkdir mnt && mount /dev/nbd0p1 mnt && cp mnt/boot/initrd.img mnt/boot/vmlinuz . && sync
umount /dev/nbd0p1 && nbd-client -d /dev/nbd0 && rmdir mnt && rm -f initrd.gz

# Run
qemu-system-s390x \
    -M s390-ccw-virtio \
    -m 2G \
    -kernel vmlinuz \
    -append "root=/dev/vda1" \
    -initrd initrd.img \
    -drive file=disk.qcow2,if=none,format=qcow2,id=hd0 \
    -device virtio-blk-ccw,drive=hd0,id=virtio-disk0 \
    -net nic,macaddr=52:54:00:fa:ce:18,model=virtio \
    -net user,hostfwd=tcp:127.0.0.1:2222-:22,id=net0 \
    -nographic
```
