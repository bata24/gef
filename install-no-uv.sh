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

TMP_DIR=$(mktemp -d)
cleanup() {
    rm -rf "${TMP_DIR}" "${GEF_DIR}/.gef.py.tmp"
}
trap cleanup 0 HUP INT TERM


echo "[+] Privilege check"
if [ "$(id -u)" = "0" ]; then
    run_as_root() { "$@"; }
else
    command -v sudo >/dev/null 2>&1 || fail "sudo is required to install system packages. Install it as root first."
    run_as_root() { sudo "$@"; }
fi


echo "[+] Check if another GEF is installed"
[ ! -e "${GEF_DIR}/gef.py" ] || fail "${GEF_DIR}/gef.py already exists. Please delete or rename it."
if [ -f "${GDBINIT}" ] && ! grep -Fqx "${STARTUP_COMMAND}" "${GDBINIT}" && grep -Eq '^[[:space:]]*(python .*from gef import|source[[:space:]]+.*gef\.py)' "${GDBINIT}"; then
    fail "Another GEF startup command exists in ${GDBINIT}."
fi


echo "[+] Create GEF directory"
mkdir -p "${GEF_DIR}/bin"


# binwalk is omitted because it requires many packages and takes a long time to install.
echo "[+] Install system packages"
if command -v apt-get >/dev/null 2>&1; then
    apt_install() { run_as_root env DEBIAN_FRONTEND=noninteractive apt-get install -y "$@"; }

    run_as_root apt-get update
    apt_install tzdata gdb-multiarch wget unzip binutils python3-dev gcc make ruby-dev git file colordiff imagemagick python3-pip

    # Installing bpftool fails inside a container, so it is excluded there.
    [ -f /.dockerenv ] || apt_install bpftool

    echo "[+] Install ceccomp"
    if ! command -v ceccomp >/dev/null 2>&1; then
        CECCOMP_ARCH=$(dpkg --print-architecture)
        if apt-cache show ceccomp >/dev/null 2>&1; then
            apt_install ceccomp
        elif ! dpkg --compare-versions "$(dpkg-query -W -f='${Version}' libc6)" ge 2.38; then
            echo "[!] Skip ceccomp: glibc 2.38 or newer is required."
        elif wget -q "https://deb.debian.org/debian/pool/main/c/ceccomp/ceccomp_4.2.2-1_${CECCOMP_ARCH}.deb" -O "${TMP_DIR}/ceccomp.deb"; then
            apt_install "${TMP_DIR}/ceccomp.deb"
        else
            echo "[!] Skip ceccomp: no prebuilt package for ${CECCOMP_ARCH}."
        fi
    fi
elif command -v pacman >/dev/null 2>&1; then
    # Arch Linux does not support partial upgrades.
    run_as_root pacman -Syu --needed --noconfirm tzdata gdb wget unzip binutils python gcc make ruby git file colordiff imagemagick ceccomp python-pip

    [ -f /.dockerenv ] || run_as_root pacman -S --needed --noconfirm bpf
else
    fail "Supported package managers are apt-get and pacman."
fi


echo "[+] pip3"
if python3 -m pip install --help | grep -q -- '--break-system-packages'; then
    pip_install() { run_as_root python3 -m pip install --break-system-packages "$@"; }
else
    pip_install() { run_as_root python3 -m pip install "$@"; }
fi
pip_install --upgrade --ignore-installed pip
pip_install "filebytes @ git+https://github.com/sashs/filebytes.git" setuptools unicorn capstone ropper keystone-engine magika angr pillow pyzbar cffi gmpy2


echo "[+] Install one_gadget"
if ! command -v one_gadget >/dev/null 2>&1; then
    gem install --no-document --install-dir "${GEF_DIR}/gems" --bindir "${GEF_DIR}/gems/bin" one_gadget
    # Expand paths when the launcher runs, so it also works after relocation.
    cat > "${GEF_DIR}/bin/one_gadget" <<'LAUNCHER'
#!/bin/sh
set -eu
GEF_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
GEM_HOME="${GEF_DIR}/gems" GEM_PATH="${GEF_DIR}/gems" exec "${GEF_DIR}/gems/bin/one_gadget" "$@"
LAUNCHER
    chmod +x "${GEF_DIR}/bin/one_gadget"
fi


echo "[+] Install rp++"
if [ "$(uname -m)" = "x86_64" ] && ! command -v rp-lin >/dev/null 2>&1 && [ ! -e "${GEF_DIR}/bin/rp-lin" ]; then
    wget -q "https://github.com/0vercl0k/rp/releases/download/v2.1.5/rp-lin-clang.zip" -O "${TMP_DIR}/rp-lin-clang.zip"
    unzip "${TMP_DIR}/rp-lin-clang.zip" -d "${GEF_DIR}/bin"
fi


echo "[+] Download GEF"
wget -q "https://raw.githubusercontent.com/bata24/gef/dev/gef.py" -O "${GEF_DIR}/.gef.py.tmp"
[ -s "${GEF_DIR}/.gef.py.tmp" ] || fail "Downloading ${GEF_DIR}/gef.py failed."
mv "${GEF_DIR}/.gef.py.tmp" "${GEF_DIR}/gef.py"


echo "[+] Setup GEF"
if ! grep -Fqx "${STARTUP_COMMAND}" "${GDBINIT}" 2>/dev/null; then
    printf '%s\n' "${STARTUP_COMMAND}" >> "${GDBINIT}"
fi


echo "[+] INSTALLATION SUCCESSFUL"
