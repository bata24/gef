#!/bin/sh
set -eu

GEF_URL="https://raw.githubusercontent.com/bata24/gef/dev/gef.py"
if [ -z "${HOME:-}" ]; then
    if [ "$(id -u)" = "0" ]; then
        export HOME="/root"
    else
        echo "[-] HOME is not set." >&2
        exit 1
    fi
fi
GEF_DIR="${GEF_INSTALL_DIR:-${HOME}/.gef}"
GEF_PATH="${GEF_DIR}/gef.py"
GDBINIT_PATH="${HOME}/.gdbinit"
GEF_TMP=""

fail() {
    echo "[-] $*" >&2
    exit 1
}

cleanup() {
    if [ -n "${GEF_TMP}" ]; then
        rm -f "${GEF_TMP}"
    fi
}
trap cleanup 0 HUP INT TERM

echo "[+] Initialize"
case "${GEF_DIR}" in
    /*) ;;
    *) fail "GEF_INSTALL_DIR must be an absolute path: ${GEF_DIR}" ;;
esac

echo "[+] Check if another GEF is installed"
if [ -e "${GEF_PATH}" ]; then
    fail "${GEF_PATH} already exists. Please delete or rename it."
fi

STARTUP_COMMAND="python sys.path.insert(0, \"${GEF_DIR}\"); from gef import *; Gef.main()"
ADD_STARTUP_COMMAND=1
if [ -f "${GDBINIT_PATH}" ]; then
    if grep -Fqx "${STARTUP_COMMAND}" "${GDBINIT_PATH}"; then
        ADD_STARTUP_COMMAND=0
    elif grep -Eq '^[[:space:]]*(python .*from gef import|source[[:space:]]+.*gef\.py)' "${GDBINIT_PATH}"; then
        fail "Another GEF startup command exists in ${GDBINIT_PATH}."
    fi
fi

echo "[+] Create GEF directory"
mkdir -p "${GEF_DIR}"

echo "[+] Download GEF"
GEF_TMP=$(mktemp "${GEF_DIR}/.gef.py.XXXXXX")
wget -q "${GEF_URL}" -O "${GEF_TMP}"
if [ ! -s "${GEF_TMP}" ]; then
    fail "Downloading ${GEF_PATH} failed."
fi
mv "${GEF_TMP}" "${GEF_PATH}"
GEF_TMP=""

echo "[+] Setup GEF"
if [ "${ADD_STARTUP_COMMAND}" -eq 1 ]; then
    printf '%s\n' "${STARTUP_COMMAND}" >> "${GDBINIT_PATH}"
fi

echo "[+] INSTALLATION SUCCESSFUL"
