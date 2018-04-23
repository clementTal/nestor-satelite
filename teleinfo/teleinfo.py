#!/usr/bin/python

import serial
import paho.mqtt.client as mqtt
import os
import logging

logging.basicConfig(filename='/home/pi/teleinfo/teleinfo.log',level=logging.WARNING)


serialdev = '/dev/serial0'
broker = "MQTT_PBRAOCKER_IP"
port = MQTT_PORT
user = "USERNAME"
passw = "PASSWORD"

#MQTT callbacks
def on_connect(mqttc, obj, flags, rc):
    if rc==0:
        mqttc.connected_flag=True
        logging.info("connected to MQTT")
        mqttc.subscribe("cmnd/teleinfo/heater", 1)
    else:
        logging.warning("Bad MQTT connection, Returned code=",rc)
        mqttc.connected_flag=False
      
def on_disconnect(mqttc, userdata, rc):
    logging.error("disconnecting reason  "  +str(rc))
    mqttc.connected_flag=False
    mqttc.disconnect_flag=True

def on_publish(mqttc, obj, mid):
    logging.info("mid: "+str(mid))
  
def on_message(client, userdata, message):
    logging.warning("message received " + str(message.payload.decode("utf-8")))
    logging.warning("message topic=" + str(message.topic))
    logging.warning("message qos=" + str(message.qos))
    logging.warning("message retain flag=" + str(message.retain))
    
def on_log(client, userdata, level, buf):
    logging.info("log: " + str(buf))

def cleanup():
    logging.error("Ending and cleaning up")
    ser.close()
      
def teleinfo(mqttc):
    ser.flushInput()
    while True:
        line = ser.readline()
        list = line.split(" ")
        if len(list) > 1:
            name = list[0].rstrip()
            data = list[1].rstrip()
            if mqttc.connected_flag:
              mqttc.publish("stat/teleinfo/"+ name, data)
        pass
    mqttc.loop_stop()
    mqttc.disconnect()
    
try:
    #create an mqtt mqttc
    mqttc = mqtt.Client(client_id="teleinfo")
    mqttc.username_pw_set(user,passw)
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_message=on_message
    mqttc.on_log = on_log
    mqttc.connect(host=broker, port=port)
    mqttc.loop_start()
    logging.info("Connecting... " + serialdev)
    ser = serial.Serial(serialdev, 1200, 7, 'E', 1, timeout=1)
    while not getattr(mqttc, 'connected_flag', 'False'):
        logging.info("wating for connection ok")
    logging.info("connection ok !")
    teleinfo(mqttc)
except (KeyboardInterrupt):
    logging.error("Interrupt received")
    cleanup()
except (RuntimeError):
    logging.error("uh-oh! time to die")
    cleanup()
except:
   logging.error("stoped")
   cleanup()