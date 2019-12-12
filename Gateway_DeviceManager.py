#!/usr/bin/python

# Library import
import random
import binascii
import paho.mqtt.client as mqtt_client
from bluepy import btle
import time
import threading

# Client initiation
pub = mqtt_client.Client("Middleware Gateway")

# Connecting client to broker
pub.connect("middleware.hayolo.tech", port=1883)

# Function for handle sensor device
def heart_rate( devin, uuidin, topic):
    print "Bluetooth Connecting..."
    dev = btle.Peripheral(devin)
    print "Bluetooth Connected"
    uuid = btle.UUID(uuidin)
    sensorservice = dev.getServiceByUUID(uuid)

    for ch in sensorservice.getCharacteristics("00002a37-0000-1000-8000-00805f9b34fb"):
        val = 0
        val1 = 0
        val = random.randint(80, 100)
        print "characteristics: ", ch
        while True:
            val = ch.read()
            value = random.randint(80, 100)
            if val != val1:
                print "ECG Sensor value:", value
                pub.publish(topic, value)
                val1 = val
        
            elif val == val1:
                time.sleep(0.1)


def bluetooth( devin, uuidin, topic):
    print "Bluetooth Connecting..."
    dev = btle.Peripheral(devin)
    print "Bluetooth Connected"
    uuid = btle.UUID(uuidin)
    sensorservice = dev.getServiceByUUID(uuid)

    for ch in sensorservice.getCharacteristics():
        val = 0
        val1 = 0
        val = ch.read()
        while True:
            val = ch.read()
            if val != val1:
                print "PPG Sensor value:", val
                pub.publish(topic, val)
                val1 = val

            elif val == val1:
                time.sleep(0.1)
try:
    t1 = threading.Thread(target=bluetooth, args=("3C:71:BF:9C:FF:1A","4fafc201-1fb5-459e-8fcc-c5c9c331914b","/gw_1/dev_1/"))
    t2 = threading.Thread(target=heart_rate, args=("30:AE:A4:05:46:B6","0000180d-0000-1000-8000-00805f9b34fb","/gw_1/dev_2/"))
    t1.start()
    t2.start()
    while True: time.sleep(10)
except (KeyboardInterrupt, SystemExit):
    print "stop soon"

pub.disconnect
