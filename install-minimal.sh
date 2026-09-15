#!/bin/sh
set -eu


fail() {
    echo "[-] $*" >&2
    exit 1
}


echo "[+] Initialize"
if [ -z "${HOME:-}" ]; then
    [ "$(id -u)" = "0" ] || fail "HOME is not set."
    export HOME="/root"
fi

GEF_DIR="${GEF_INSTALL_DIR:-${HOME}/.gef}"
GDBINIT="${HOME}/.gdbinit"
STARTUP_COMMAND="python sys.path.insert(0, \"${GEF_DIR}\"); from gef import *; Gef.main()"

case "${GEF_DIR}" in
    /*) ;;
    *) fail "GEF_INSTALL_DIR must be an absolute path: ${GEF_DIR}" ;;
esac

cleanup() {
    rm -f "${GEF_DIR}/.gef.py.tmp"
}
trap cleanup 0 HUP INT TERM


echo "[+] Check if another GEF is installed"
[ ! -e "${GEF_DIR}/gef.py" ] || fail "${GEF_DIR}/gef.py already exists. Please delete or rename it."
if [ -f "${GDBINIT}" ] && ! grep -Fqx "${STARTUP_COMMAND}" "${GDBINIT}" && grep -Eq '^[[:space:]]*(python .*from gef import|source[[:space:]]+.*gef\.py)' "${GDBINIT}"; then
    fail "Another GEF startup command exists in ${GDBINIT}."
fi


echo "[+] Create GEF directory"
mkdir -p "${GEF_DIR}"


echo "[+] Download GEF"
wget -q "https://raw.githubusercontent.com/bata24/gef/dev/gef.py" -O "${GEF_DIR}/.gef.py.tmp"
[ -s "${GEF_DIR}/.gef.py.tmp" ] || fail "Downloading ${GEF_DIR}/gef.py failed."
mv "${GEF_DIR}/.gef.py.tmp" "${GEF_DIR}/gef.py"


echo "[+] Setup GEF"
if ! grep -Fqx "${STARTUP_COMMAND}" "${GDBINIT}" 2>/dev/null; then
    printf '%s\n' "${STARTUP_COMMAND}" >> "${GDBINIT}"
fi


echo "[+] INSTALLATION SUCCESSFUL"
