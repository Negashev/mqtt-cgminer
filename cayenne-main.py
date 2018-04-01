import json
import os
import time
import cayenne.client
from pycgminer import CgminerAPI

# Cayenne authentication info. This should be obtained from the Cayenne Dashboard.
MQTT_USERNAME = os.getenv('MQTT_USERNAME')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD')
MQTT_CLIENT_ID = os.getenv('MQTT_CLIENT_ID')


# The callback for when a message is received from Cayenne.
def on_message(message):
    print("message received: " + str(message))
    # If there is an error processing the message return an error string, otherwise return nothing.


cgminer = CgminerAPI(host=os.getenv('CGMINER_HOST'), port=int(os.getenv('CGMINER_PORT')))

client = cayenne.client.CayenneMQTTClient()
client.on_message = on_message
client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID)
# For a secure connection use port 8883 when calling client.begin:
# client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID, port=8883)

timestamp = 0

while True:
    client.loop()

    if (time.time() > timestamp + 5):
        STATS = cgminer.estats()['STATS'][0]
        client.celsiusWrite(1, int(STATS["temp1"]))
        client.celsiusWrite(2, int(STATS["temp2"]))

        client.virtualWrite(3, float(STATS['voltage']), cayenne.client.TYPE_VOLTAGE, cayenne.client.UNIT_VOLTS)
        client.virtualWrite(4, float(STATS["GHS 5s"]), cayenne.client.TYPE_VOLTAGE, 'GHs')
        timestamp = time.time()
