#!/bin/sh -eux

if [ ! $(id -u) = 0 ]; then
  echo "[-] Detected non-root user, install failed."
  exit 1
fi

echo "[+] apt"
apt-get update
apt-get install -y gdb-multiarch python3-pip binutils gcc ruby-dev

echo "[+] pip3"
pip3 install rpyc psutil crccheck unicorn capstone ropper keystone-engine

echo "[+] install seccomp-tools, one_gadget"
if [ "x$(which seccomp-tools)" = "x" ]; then
  gem install seccomp-tools
fi

if [ "x$(which one_gadget)" = "x" ]; then
  gem install one_gadget
fi

echo "[+] install rp++"
if [ "x$(uname -m)" = "xx86_64" ]; then
  if [ "x$(getconf LONG_BIT)" = "x64" ]; then
    if [ "x$(which rp-lin-x64)" = "x" ]; then
      wget -q https://github.com/0vercl0k/rp/releases/download/v1/rp-lin-x64 -O /usr/local/bin/rp-lin-x64
      chmod +x /usr/local/bin/rp-lin-x64
    fi
  fi
fi

if [ "x$(uname -m)" = "xx86_64" ] || [ "x$(uname -m)" = "xi686" ]; then
  if [ "x$(getconf LONG_BIT)" = "x32" ]; then
    if [ "x$(which rp-lin-x86)" = "x" ]; then
      wget -q https://github.com/0vercl0k/rp/releases/download/v1/rp-lin-x86 -O /usr/local/bin/rp-lin-x86
      chmod +x /usr/local/bin/rp-lin-x86
    fi
  fi
fi

echo "[+] download gef"
wget -q https://raw.githubusercontent.com/bata24/gef/dev/gef.py -O /root/.gdbinit-gef.py

echo "[+] setup gef"
STARTUP_COMMAND="source ~/.gdbinit-gef.py"
if [ ! -e /root/.gdbinit ] || [ "x$(grep "$STARTUP_COMMAND" /root/.gdbinit)" = "x" ]; then
  echo "$STARTUP_COMMAND" >> /root/.gdbinit
fi

exit 0
