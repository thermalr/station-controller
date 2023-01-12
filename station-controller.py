import json
import requests
import paho.mqtt.client as paho
import RPi.GPIO as GPIO
import time
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

###############################################################################
# Setup GPIO
###############################################################################
lock_pin = 17
sens_pin = 4

time_delay = 5
time_lock = 0.5

GPIO.setmode(GPIO.BCM)

GPIO.setup(lock_pin,GPIO.OUT)
GPIO.setup(sens_pin,GPIO.IN)

###############################################################################
# Bicycle lock/unlock APIs
###############################################################################
def on_bicycle_unlock(bike_id):
    url = "https://us-central1-ev-firestore-2019.cloudfunctions.net/onBicycleUnlock?bicycleId=" + bike_id
    headers = {}
    payload = json.dumps({})
    response = requests.post(url, headers=headers, data=payload, verify=False)
    return response.json()

def on_bicycle_lock(bike_id):
    url = "https://us-central1-ev-firestore-2019.cloudfunctions.net/onBicycleLock?bicycleId=" + bike_id
    headers = {}
    payload = json.dumps({})
    response = requests.post(url, headers=headers, data=payload, verify=False)
    return response.json()

###############################################################################
# MQTT Listener Implementation
###############################################################################
def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+ str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    payload = json.loads(msg.payload.decode('utf-8'))
    GPIO.output(lock_pin, GPIO.HIGH) # TODO: change here
    on_bicycle_unlock(payload["bicycleId"])

client = paho.Client()
client.on_subscribe = on_subscribe
client.on_message = on_message
client.connect('broker.hivemq.com', 1883)
client.subscribe('ev/bikes', qos=1)
client.loop_forever()
