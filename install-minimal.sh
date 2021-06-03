#!/bin/sh -eux

if [ ! $(id -u) = 0 ]; then
  echo "[-] Detected non-root user, install failed."
  exit 1
fi

echo "[+] apt"
apt-get update
apt-get install -y gdb-multiarch python3-pip binutils gcc

echo "[+] pip3"
pip3 install rpyc psutil

echo "[+] download gef"
wget -q https://raw.githubusercontent.com/bata24/gef/dev/gef.py -O /root/.gdbinit-gef.py

echo "[+] setup gef"
STARTUP_COMMAND="source ~/.gdbinit-gef.py"
if [ ! -e /root/.gdbinit ] || [ "x$(grep "$STARTUP_COMMAND" /root/.gdbinit)" = "x" ]; then
  echo "$STARTUP_COMMAND" >> /root/.gdbinit
fi

exit 0
