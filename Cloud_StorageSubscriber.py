#!/usr/bin/python2

# Import paho mqtt library
import paho.mqtt.client as mqtt
import datetime
from pymongo import MongoClient

# Initiation mqtt client
sub = mqtt.Client(transport='websockets')

client = MongoClient('127.0.0.1', 27017)
db = client.test

# Connecting subscriber to broker
sub.connect("127.0.0.1", port=9001)
print ("subsc")

# Subscribe to a topic
sub.subscribe("/gw_1/dev_1/")
sub.subscribe("/gw_1/dev_2/")

# Buat fungsi untuk handle ketika ada message masuk
def handle_message(mqttc, obj, msg):
    topic = msg.topic
    split1 = topic.split("/")
    payload = msg.payload.decode('ascii')
    print("Topik : "+topic+" Payload : "+payload+" Gateway : "+split1[1]+" Device : "+split1[2])
    db.sensor.insert_one({
        "TIMESTAMP": datetime.datetime.now(),
        "Gateway": split1[1],
        "Device": split1[2],
        "value": payload,			
	})

# Daftarkan fungsi untuk handle message masuk
sub.on_message = handle_message

# Looping supaya subscribernya tetap jalan
sub.loop_forever()
