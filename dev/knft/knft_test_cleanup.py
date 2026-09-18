#!/bin/sh
set -eu

TABLE_A="gef_knft_test_a"
TABLE_B="gef_knft_test_b"

if [ "$(id -u)" -ne 0 ]; then
    echo "rootで実行してください" >&2
    exit 1
fi

if ! command -v nft >/dev/null 2>&1; then
    echo "nftコマンドが見つかりません" >&2
    exit 1
fi

# setup側で作成したtableを削除する。flowtableやchild objectもtableと一緒に消える。
if nft list table inet "$TABLE_A" >/dev/null 2>&1; then
    nft delete table inet "$TABLE_A"
    echo "inet $TABLE_Aを削除しました"
else
    echo "inet $TABLE_Aは存在しません"
fi

if nft list table ip "$TABLE_B" >/dev/null 2>&1; then
    nft delete table ip "$TABLE_B"
    echo "ip $TABLE_Bを削除しました"
else
    echo "ip $TABLE_Bは存在しません"
fi
