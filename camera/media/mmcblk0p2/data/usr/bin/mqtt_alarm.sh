#!/bin/sh
# alarm.sh
user=`sed -n 1p /etc/mqtt`
pass=`sed -n 2p /etc/mqtt`
url=`sed -n 3p /etc/mqtt`
port=`sed -n 4p /etc/mqtt`
alarm=`sed -n 5p /etc/mqtt`
exec mosquitto_pub -h "$url" -p "$port" -u "$user" -P "$pass" -t "$alarm" -i 'xiaofang' -m "$1"