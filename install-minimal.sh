#!/bin/sh -ex

echo "[+] Initialize"
if [ -z "${GDBINIT_PATH}" ]; then
    GDBINIT_PATH="/root/.gdbinit"
fi
GEF_PATH="${GDBINIT_PATH}-gef.py"

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
exit 0
