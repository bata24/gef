#!/bin/sh
set -eu

GEF_URL="https://raw.githubusercontent.com/bata24/gef/dev/gef.py"
RP_URL="https://github.com/0vercl0k/rp/releases/download/v2.1.5/rp-lin-clang.zip"
CECCOMP_DEB_VERSION="4.2.2-1"
CECCOMP_DEB_BASE_URL="https://deb.debian.org/debian/pool/main/c/ceccomp"
ONE_GADGET_VERSION="1.9.0"
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
GEF_BIN_DIR="${GEF_DIR}/bin"
GEF_GEM_DIR="${GEF_DIR}/gems"
GDBINIT_PATH="${HOME}/.gdbinit"
GEF_TMP=""
RP_TMP=""
CECCOMP_TMP=""

fail() {
    echo "[-] $*" >&2
    exit 1
}

run_as_root() {
    if [ "$(id -u)" = "0" ]; then
        "$@"
    else
        sudo "$@"
    fi
}

cleanup() {
    if [ -n "${GEF_TMP}" ]; then
        rm -f "${GEF_TMP}"
    fi
    if [ -n "${RP_TMP}" ]; then
        rm -f "${RP_TMP}"
    fi
    if [ -n "${CECCOMP_TMP}" ]; then
        rm -f "${CECCOMP_TMP}"
    fi
}
trap cleanup 0 HUP INT TERM

echo "[+] Initialize"
case "${GEF_DIR}" in
    /*) ;;
    *) fail "GEF_INSTALL_DIR must be an absolute path: ${GEF_DIR}" ;;
esac

echo "[+] Privilege check"
if [ "$(id -u)" != "0" ] && ! command -v sudo >/dev/null 2>&1; then
    fail "sudo is required to install system packages. Install it as root first."
fi

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
mkdir -p "${GEF_BIN_DIR}"

echo "[+] Install system packages"
if command -v apt-get >/dev/null 2>&1; then
    run_as_root apt-get update
    run_as_root env DEBIAN_FRONTEND=noninteractive apt-get install -y \
        tzdata gdb-multiarch wget unzip \
        binutils python3-pip ruby-dev git file colordiff imagemagick

    # Installing bpftool fails inside a container, so it is excluded there.
    if [ ! -f /.dockerenv ]; then
        run_as_root apt-get install -y bpftool
    fi

    echo "[+] Install ceccomp"
    if ! command -v ceccomp >/dev/null 2>&1; then
        if apt-cache show ceccomp >/dev/null 2>&1; then
            run_as_root env DEBIAN_FRONTEND=noninteractive apt-get install -y ceccomp
        elif dpkg --compare-versions "$(dpkg-query -W -f='${Version}' libc6)" ge 2.38; then
            CECCOMP_ARCH=$(dpkg --print-architecture)
            CECCOMP_TMP=$(mktemp /tmp/ceccomp.XXXXXX.deb)
            wget -q "${CECCOMP_DEB_BASE_URL}/ceccomp_${CECCOMP_DEB_VERSION}_${CECCOMP_ARCH}.deb" -O "${CECCOMP_TMP}"
            run_as_root env DEBIAN_FRONTEND=noninteractive apt-get install -y "${CECCOMP_TMP}"
            rm -f "${CECCOMP_TMP}"
            CECCOMP_TMP=""
        else
            echo "[!] Skip ceccomp: glibc 2.38 or newer is required."
        fi
    fi
elif command -v pacman >/dev/null 2>&1; then
    # Arch Linux does not support partial upgrades.
    run_as_root pacman -Syu --needed --noconfirm \
        tzdata gdb wget unzip binutils python python-pip \
        gcc make ruby git file colordiff imagemagick ceccomp

    if [ ! -f /.dockerenv ]; then
        run_as_root pacman -S --needed --noconfirm bpf
    fi
else
    fail "Supported package managers are apt-get and pacman."
fi

# binwalk is omitted because it requires many packages and takes a long time to install.

echo "[+] pip3"
PIP_OPTIONS=""
if python3 -m pip install --help | grep -q -- '--break-system-packages'; then
    PIP_OPTIONS="--break-system-packages"
fi
# PIP_OPTIONS is either empty or a single trusted option.
# shellcheck disable=SC2086
run_as_root python3 -m pip install ${PIP_OPTIONS} --upgrade --ignore-installed pip
# shellcheck disable=SC2086
run_as_root python3 -m pip install ${PIP_OPTIONS} \
    "filebytes @ git+https://github.com/sashs/filebytes.git" \
    setuptools unicorn capstone ropper keystone-engine magika \
    angr pillow pyzbar cffi gmpy2

echo "[+] Install one_gadget"
if ! command -v one_gadget >/dev/null 2>&1; then
    gem install --no-document --install-dir "${GEF_GEM_DIR}" --bindir "${GEF_GEM_DIR}/bin" one_gadget -v "${ONE_GADGET_VERSION}"
    # Expand paths when the launcher runs, so it also works after relocation.
    # shellcheck disable=SC2016
    printf '%s\n' '#!/bin/sh
set -eu
GEF_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
GEM_HOME="${GEF_DIR}/gems" GEM_PATH="${GEF_DIR}/gems" exec "${GEF_DIR}/gems/bin/one_gadget" "$@"' > "${GEF_BIN_DIR}/one_gadget"
    chmod +x "${GEF_BIN_DIR}/one_gadget"
fi

echo "[+] Install rp++"
if [ "$(uname -m)" = "x86_64" ] \
    && ! command -v rp-lin >/dev/null 2>&1 \
    && [ ! -e "${GEF_BIN_DIR}/rp-lin" ]; then
    RP_TMP=$(mktemp /tmp/rp-lin-clang.XXXXXX.zip)
    wget -q "${RP_URL}" -O "${RP_TMP}"
    unzip "${RP_TMP}" -d "${GEF_BIN_DIR}"
    rm -f "${RP_TMP}"
    RP_TMP=""
fi

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
