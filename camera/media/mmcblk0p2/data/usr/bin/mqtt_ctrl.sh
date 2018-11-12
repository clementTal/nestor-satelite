#!/bin/sh
# mqtt_ctrl.sh
user=`sed -n 1p /etc/mqtt`
pass=`sed -n 2p /etc/mqtt`
url=`sed -n 3p /etc/mqtt`
port=`sed -n 4p /etc/mqtt`
ctrl=`sed -n 6p /etc/mqtt`
status_ctrl=`sed -n 9p /etc/mqtt`

mosquitto_sub -h "$url" -p "$port" -u "$user" -P "$pass" -t "$ctrl"  | while read mqttcmd;
do
  /media/mmcblk0p2/data/etc/scripts/20-rtsp-server stop
  echo "Start or stop service with $mqttcmd"
  /media/mmcblk0p2/data/etc/scripts/20-rtsp-server $mqttcmd
  usleep 500000
  status=`ps | grep snx_snapshot_v3`
  if echo "$status" | grep -q "snx_snapshot_v3 -m"; then
    echo "ON $status"
    sh /media/mmcblk0p2/data/usr/bin/mqtt_switch.sh "ON" &
  else
    echo "OFF $status"
    sh /media/mmcblk0p2/data/usr/bin/mqtt_switch.sh "OFF" &
  fi
  echo "ok"
  usleep 5000000
  sh /media/mmcblk0p2/data/usr/bin/mqtt_send_picture.sh /media/mmcblk0p2/data/usr/bin/not-home.jpg
done


# mosquitto_sub -h "$url" -p "$port" -u "$user" -P "$pass" -i "xiaofang" -t "$status_ctrl"  | while read mqttcmd;
# do
  # status=`ps | grep snx_snapshot_v3`
  # if echo "$status" | grep -q "snx_snapshot_v3 -m"; then
    # echo "ON $status"
    # sh /media/mmcblk0p2/data/usr/bin/mqtt_switch.sh "ON" &
  # else
    # echo "OFF $status"
    # sh /media/mmcblk0p2/data/usr/bin/mqtt_switch.sh "OFF" &
  # fi
  # echo "ok"
# done
