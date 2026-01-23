#!/bin/sh -ex

echo "[+] Initialize"
GDBINIT_PATH="/root/.gdbinit"
GEF_DIR="/root/.gef"
GEF_PATH="${GEF_DIR}/gef.py"
GEF_VENV_CONF_PATH="${GEF_DIR}/gef.venv.conf"
GEF_VENV_PATH="${GEF_DIR}/.venv-gef"
GEF_VENV_BIN_PATH="${GEF_VENV_PATH}/bin"

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
apt-get install -y binutils python3-dev gcc make ruby-dev git file colordiff imagemagick

# Since installing bpftool fails inside a container, it is excluded.
if [ ! -f /.dockerenv ]; then
    apt-get install -y bpftool
fi

# Installing binwalk requires a large number of packages and takes a significant amount of time,
# so please enable it only when necessary.
#apt-get install -y binwalk

echo "[+] Install uv"
if [ -z "$(command -v uv)" ]; then
    wget -qO- https://astral.sh/uv/install.sh | sh
    . $HOME/.local/bin/env
fi

echo "[+] Setup venv"
if [ ! -e "${GEF_VENV_PATH}" ]; then
    uv venv "${GEF_VENV_PATH}"
fi
. "${GEF_VENV_PATH}/bin/activate"

echo "[+] pip3"
uv pip install setuptools crccheck unicorn capstone ropper keystone-engine tqdm magika codext angr pycryptodome pillow pyzbar

echo "[+] Install seccomp-tools"
if [ -z "$(command -v seccomp-tools)" ]; then
    gem install -i "${GEF_VENV_PATH}" seccomp-tools
fi

echo "[+] Install one_gadget"
if [ -z "$(command -v one_gadget)" ]; then
    gem install -i "${GEF_VENV_PATH}" one_gadget
fi

echo "[+] Install rp++"
if [ "$(uname -m)" = "x86_64" ]; then
    if [ -z "$(command -v rp-lin)" ]; then
        wget -q https://github.com/0vercl0k/rp/releases/download/v2.1.5/rp-lin-clang.zip -P /tmp
        unzip /tmp/rp-lin-clang.zip -d "${GEF_VENV_BIN_PATH}"
        rm /tmp/rp-lin-clang.zip
    fi
fi

echo "[+] Install vmlinux-to-elf"
if [ -z "$(command -v vmlinux-to-elf)" ]; then
    uv tool install git+https://github.com/marin-m/vmlinux-to-elf
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

echo "[+] Setup venv path hint file"
GEF_VENV_SYS_PATH=$(python3 -c 'import sys,subprocess;a=subprocess.getoutput("gdb-multiarch -q -nx -ex \"pi sys.path\" -ex q");print(":".join(set(sys.path)-set(eval(a))-set([""])))')
echo "GEF_VENV_GEM_HOME=${GEF_VENV_PATH}" >> ${GEF_VENV_CONF_PATH}
echo "GEF_VENV_SYS_PATH=${GEF_VENV_SYS_PATH}" >> ${GEF_VENV_CONF_PATH}
echo "GEF_VENV_BIN_PATH=${GEF_VENV_BIN_PATH}" >> ${GEF_VENV_CONF_PATH}

echo "[+] INSTALLATION SUCCESSFUL"
exit 0
