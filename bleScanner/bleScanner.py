from bluepy.btle import Scanner, DefaultDelegate
import paho.mqtt.client as mqtt
import logging



broker = "MQTT_PBRAOCKER_IP"
port = MQTT_PORT
user = "USERNAME"
passw = "PASSWORD"
TileHome = False

logging.basicConfig(filename='/home/pi/bleScanner/bleScanner.log',level=logging.WARNING)

#MQTT callbacks
def on_connect(mqttc, obj, flags, rc):
    if rc==0:
        mqttc.connected_flag=True
        logging.info("connected to MQTT")
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

def bleScanner(mqttc):
  scanner = Scanner()
  while True:
    devices = scanner.scan(10.0)
    TileHome = "OFF"
    for dev in devices:
      if dev.getValueText(9) and dev.getValueText(9) == "Tile":
        TileHome = "ON"
    if mqttc.connected_flag:
        logging.info("publish " + TileHome)
        mqttc.publish("stat/precence/tile", TileHome)

try:
    #create an mqtt mqttc
    mqttc = mqtt.Client(client_id="bleScanner")
    mqttc.username_pw_set(user,passw)
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_message=on_message
    mqttc.on_log = on_log
    mqttc.connect(host=broker, port=port)
    mqttc.loop_start()
    while not getattr(mqttc, 'connected_flag', 'False'):
        logging.info("wating for connection ok")
    logging.info("connection ok !")
    bleScanner(mqttc)
except (KeyboardInterrupt):
    logging.error("Interrupt received")
    cleanup()
except (RuntimeError):
    logging.error("uh-oh! time to die")
    cleanup()
except:
   logging.error("stoped")
   cleanup()


