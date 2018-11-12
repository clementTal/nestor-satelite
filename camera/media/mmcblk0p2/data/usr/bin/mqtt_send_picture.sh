#!/bin/sh
# send.sh
user=`sed -n 1p /etc/mqtt`
pass=`sed -n 2p /etc/mqtt`
url=`sed -n 3p /etc/mqtt`
port=`sed -n 4p /etc/mqtt`
picture=`sed -n 7p /etc/mqtt`

mosquitto_pub -h "$url" -p "$port" -u "$user" -P "$pass" -t "$picture" -f "$1"
#exec usleep 125000 # limit to circa 8 FPS