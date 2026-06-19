#!/bin/sh
set -ex

echo "[+] Initialize"
GDBINIT_PATH="/root/.gdbinit"
GEF_DIR="/root/.gef"
GEF_PATH="${GEF_DIR}/gef.py"

echo "[+] User check"
if [ "$(id -u)" != "0" ]; then
    echo "[-] Detected non-root user."
    echo "[-] INSTALLATION FAILED"
    exit 1
fi

echo "[+] Check if another gef is installed"
if [ -e "${GEF_PATH}" ]; then
    echo "[-] ${GEF_PATH} already exists. Please delete or rename."
    echo "[-] INSTALLATION FAILED"
    exit 1
fi

echo "[+] Create .gef directory"
if [ ! -e "${GEF_DIR}" ]; then
    mkdir -p "${GEF_DIR}"
fi

echo "[+] apt"
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata
apt-get install -y gdb-multiarch wget unzip
apt-get install -y binutils python3-pip ruby-dev git file colordiff imagemagick

# bpftool is no longer a standalone package; it ships in linux-tools-$(uname -r).
# That package is tied to the running kernel and is frequently unavailable inside
# containers (the host kernel's linux-tools may not exist in the image's repos),

echo "[+] Install bpftool"
if [ -z "$(command -v bpftool)" ]; then
    KREL="$(uname -r)"
    if ! apt-get install -y "linux-tools-${KREL}"; then
        # Fall back to the generic meta-package, then the common linux-tools pkg.
        apt-get install -y linux-tools-common
    fi
fi

# Installing binwalk requires a large number of packages and takes a significant amount of time,
# so please enable it only when necessary.
#apt-get install -y binwalk

echo "[+] pip3"
pip3 install "filebytes @ git+https://github.com/sashs/filebytes.git" # for Ubuntu 26.04
pip3 install setuptools crccheck unicorn capstone ropper keystone-engine tqdm magika codext angr pillow pyzbar cffi gmpy2

# The GEF installer installs `seccomp-tools` if neither `ceccomp` nor `seccomp-tools` is found.
# I recomend `ceccomp`, but its build is not simple. Install it manually if needed.
echo "[+] Install seccomp-tools"
if [ -z "$(command -v seccomp-tools)" ] && [ -z "$(command -v ceccomp)" ]; then
    gem install seccomp-tools
fi

echo "[+] Install one_gadget"
if [ -z "$(command -v one_gadget)" ]; then
    gem install one_gadget
fi

echo "[+] Install rp++"
if [ "$(uname -m)" = "x86_64" ]; then
    if [ -z "$(command -v rp-lin)" ] && [ ! -e /usr/local/bin/rp-lin ]; then
        wget -q https://github.com/0vercl0k/rp/releases/download/v2.1.5/rp-lin-clang.zip -P /tmp
        unzip /tmp/rp-lin-clang.zip -d /usr/local/bin/
        rm /tmp/rp-lin-clang.zip
    fi
fi

echo "[+] Download gef"
wget -q https://raw.githubusercontent.com/bata24/gef/dev/gef.py -O "${GEF_PATH}"
if [ ! -s "${GEF_PATH}" ]; then
    echo "[-] Downloading ${GEF_PATH} failed."
    rm -f "${GEF_PATH}"
    echo "[-] INSTALLATION FAILED"
    exit 1
fi

echo "[+] Setup gef"
STARTUP_COMMAND="python sys.path.insert(0, \"${GEF_DIR}\"); from gef import *; Gef.main()"
if [ ! -e "${GDBINIT_PATH}" ] || [ -z "$(grep "from gef import" "${GDBINIT_PATH}")" ]; then
    echo "${STARTUP_COMMAND}" >> "${GDBINIT_PATH}"
fi

echo "[+] INSTALLATION SUCCESSFUL"
exit 0
