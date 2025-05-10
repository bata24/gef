#!/bin/sh -ex

echo "[+] Initialize"
if [ -z "${GDBINIT_PATH}" ]; then
    GDBINIT_PATH="/root/.gdbinit"
fi
GEF_PATH="${GDBINIT_PATH}-gef.py"
GEF_VENV_PATH="$(dirname ${GDBINIT_PATH})/.venv-gef"

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

echo "[+] apt"
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata
apt-get install -y gdb-multiarch wget
apt-get install -y binutils python3-dev gcc ruby-dev git file colordiff imagemagick
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
        wget -q https://github.com/0vercl0k/rp/releases/download/v2.1.4/rp-lin-clang.zip -P /tmp
        unzip /tmp/rp-lin-clang.zip -d "${GEF_VENV_PATH}/bin"
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
STARTUP_COMMAND="source ${GEF_PATH}"
if [ ! -e "${GDBINIT_PATH}" ] || [ -z "$(grep "${STARTUP_COMMAND}" "${GDBINIT_PATH}")" ]; then
    echo "${STARTUP_COMMAND}" >> "${GDBINIT_PATH}"
fi

echo "[+] INSTALLATION SUCCESSFUL"
echo "[+] Run 'source ${GEF_VENV_PATH}/bin/activate' before starting gdb."
exit 0
