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
apt-get install -y gdb-multiarch wget
apt-get install -y binutils python3-dev gcc make ruby-dev git file colordiff imagemagick
apt-get install -y binwalk

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
uv pip install setuptools crccheck unicorn capstone ropper keystone-engine tqdm magika codext angr==9.2.154 pycryptodome pillow pyzbar
# Since angr version 9.2.156, installing via pip or uv triggers a build process.
# This requires Rust to be installed and can take around 10 minutes to complete, which is not intended.
# To ensure the expected behavior, we pin the version to 9.2.154. See PR #115 for details.

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
        wget -q https://github.com/0vercl0k/rp/releases/download/v2.1.4/rp-lin-clang.zip -P /tmp
        unzip /tmp/rp-lin-clang.zip -d "${GEF_VENV_BIN_PATH}"
        rm /tmp/rp-lin-clang.zip
    fi
fi

echo "[+] Install vmlinux-to-elf"
if [ -z "$(command -v vmlinux-to-elf)" ]; then
    uv pip install --upgrade lz4 zstandard git+https://github.com/clubby789/python-lzo@b4e39df
    uv pip install --upgrade git+https://github.com/marin-m/vmlinux-to-elf
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
