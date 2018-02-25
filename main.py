import os
import json
from time import sleep

import paho.mqtt.client as mqtt
from pycgminer import CgminerAPI

cgminer = CgminerAPI(host=os.getenv('CGMINER_HOST'), port=int(os.getenv('CGMINER_PORT')))


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker " + os.getenv('MQTT_HOST') + ":" + os.getenv('MQTT_PORT'))
        global Connected  # Use global variable
        Connected = True  # Signal connection
    else:
        print("Connection failed")


client = mqtt.Client()
# Register connect callback
client.on_connect = on_connect
# Set access token
client.username_pw_set(os.getenv('MQTT_PASS'))
# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(os.getenv('MQTT_HOST'), int(os.getenv('MQTT_PORT')), 60)

client.loop_start()  # start the loop

try:
    while True:
        try:
            client.publish("v1/devices/me/telemetry", json.dumps(cgminer.estats()['STATS'][0]))
            sleep(int(os.getenv('SLEEP_TIME', 1)))
        except Exception as e:
            print(e)
            sleep(10)
except KeyboardInterrupt:
    client.disconnect()
    client.loop_stop()
