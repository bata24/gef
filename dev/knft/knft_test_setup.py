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

modprobe nf_tables

# 前回のテスト用tableだけを削除し、何度でも同じ状態から作れるようにする。
nft delete table inet "$TABLE_A" 2>/dev/null || true
nft delete table ip "$TABLE_B" 2>/dev/null || true

# chain / rule / set / named objectを含む基本テスト構成。
# verdictはdrop/rejectを使わず、ゲストの通信を壊しにくい内容にしている。
nft -f - <<'RULESET'
table inet gef_knft_test_a {
    counter cnt_tcp {
    }

    counter cnt_udp {
    }

    set trusted_v4 {
        type ipv4_addr
        flags interval
        elements = { 10.10.0.0/16, 192.0.2.10, 198.51.100.0/24 }
    }

    set service_ports {
        type inet_service
        elements = { 22, 80, 443, 8080 }
    }

    chain input_probe {
        type filter hook input priority 300; policy accept;

        iifname "lo" counter
        meta l4proto tcp jump tcp_path
        meta l4proto udp jump udp_path
        ip saddr @trusted_v4 counter
    }

    chain tcp_path {
        tcp dport @service_ports counter name cnt_tcp
        tcp dport 31337 limit rate 5/second counter
        ip saddr 203.0.113.0/24 tcp dport 1-1024 counter
    }

    chain udp_path {
        udp dport { 53, 123, 5353 } counter name cnt_udp
        ip daddr 224.0.0.0/4 counter
        meta length 64-1500 counter
    }
}

table ip gef_knft_test_b {
    counter cnt_misc {
    }

    set hosts {
        type ipv4_addr
        elements = { 192.0.2.1, 198.51.100.2, 203.0.113.3 }
    }

    set odd_ports {
        type inet_service
        elements = { 1, 7, 9, 19, 37 }
    }

    chain probe_a {
        ip saddr @hosts counter name cnt_misc
        tcp sport 1-1024 counter
    }

    chain probe_b {
        ip daddr @hosts counter
        udp dport @odd_ports counter
        meta l4proto tcp jump probe_a
    }
}
RULESET

# flowtableはkernel configと利用可能なnetdevに依存するため、作れる場合だけ追加する。
FLOWDEV=""
for path in /sys/class/net/*; do
    iface=${path##*/}
    [ "$iface" = "lo" ] && continue
    FLOWDEV="$iface"
    break
done

if [ -n "$FLOWDEV" ]; then
    if nft "add flowtable inet $TABLE_A ft_ingress { hook ingress priority 0; devices = { \"$FLOWDEV\" }; }" 2>/dev/null; then
        echo "flowtable ft_ingressを追加しました: device=$FLOWDEV"
    else
        echo "flowtableは追加できませんでした。基本テスト構成は登録済みです"
    fi
else
    echo "lo以外のnetdevがないためflowtableは省略しました"
fi

echo
echo "登録したテスト用ruleset:"
nft list table inet "$TABLE_A"
echo
nft list table ip "$TABLE_B"
