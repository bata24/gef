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

echo "[+] apt"
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata
apt-get install -y gdb-multiarch wget binutils python3-pip python3-venv ruby-dev git file colordiff binwalk imagemagick

echo "[+] Setup venv"
python3 -m venv -- "${GEF_VENV_PATH}"
. "${GEF_VENV_PATH}/bin/activate"

echo "[+] pip3"
pip3 install setuptools crccheck unicorn capstone ropper keystone-engine tqdm magika codext angr pycryptodome pillow pyzbar

echo "[+] Install seccomp-tools"
if [ -z "$(command -v seccomp-tools)" ]; then
    gem install seccomp-tools
fi

echo "[+] Install one_gadget"
if [ -z "$(command -v one_gadget)" ]; then
    gem install one_gadget
fi

echo "[+] Install rp++"
if [ "$(uname -m)" = "x86_64" ]; then
    if [ -z "$(command -v rp-lin)" ] && [ ! -e /usr/local/bin/rp-lin ]; then
        # v2.1.3 will cause an error on Ubuntu 22.10 or earlier.
        # The only difference between 2.1.2 and 2.1.3 is for OpenBSD compatibility and can be ignored.
        wget -q https://github.com/0vercl0k/rp/releases/download/v2.1.2/rp-lin-clang.zip -P /tmp
        unzip /tmp/rp-lin-clang.zip -d /usr/local/bin/
        chmod +x /usr/local/bin/rp-lin
        rm /tmp/rp-lin-clang.zip
    fi
fi

echo "[+] Install vmlinux-to-elf"
if [ -z "$(command -v vmlinux-to-elf)" ] && [ ! -e /usr/local/bin/vmlinux-to-elf ]; then
    pip3 install --upgrade lz4 zstandard git+https://github.com/clubby789/python-lzo@b4e39df
    pip3 install --upgrade git+https://github.com/marin-m/vmlinux-to-elf
fi

echo "[+] Download gef"
if [ -e "${GEF_PATH}" ]; then
    echo "[-] ${GEF_PATH} already exists. Please delete or rename."
    echo "[-] INSTALLATION FAILED"
    exit 1
else
    wget -q https://raw.githubusercontent.com/bata24/gef/dev/gef.py -O "${GEF_PATH}"
    if [ ! -s "${GEF_PATH}" ]; then
        echo "[-] Downloading ${GEF_PATH} failed."
        rm -f "${GEF_PATH}"
        echo "[-] INSTALLATION FAILED"
        exit 1
    fi
fi

echo "[+] Setup gef"
STARTUP_COMMAND="source ${GEF_PATH}"
if [ ! -e "${GDBINIT_PATH}" ] || [ -z "$(grep "${STARTUP_COMMAND}" "${GDBINIT_PATH}")" ]; then
    echo "${STARTUP_COMMAND}" >> "${GDBINIT_PATH}"
fi

echo "[+] INSTALLATION SUCCESSFUL"
echo "[+] Run 'source ${GEF_VENV_PATH}/bin/activate' before starting gdb."
exit 0
