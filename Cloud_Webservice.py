#!/usr/bin/python2
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_DB"] = "test"
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/test"

mongo = PyMongo(app)

@app.route("/gw_1/", methods=['GET'])
def get_sensor1():
    sensors = mongo.db.sensor
    output = []
    for q in sensors.find():
        output.append({'Generate Time' : q['TIMESTAMP'],'Gateway' : q['Gateway'],'Device' : q['Device'], 'Value' : q['value']})
    return jsonify({'result' : output})

@app.route("/gw_1/dev_1", methods=['GET'])
def get_sensor2():
    sensors = mongo.db.sensor
    output = []
    for q in sensors.find({"Device" : "dev_1"}):
       output.append({'Generate Time' : q['TIMESTAMP'],'Gateway' : q['Gateway'],'Device' : q['Device'], 'Value' : q['value']})
    return jsonify({'result' : output})

@app.route("/gw_1/dev_2", methods=['GET'])
def get_sensor3():
    sensors = mongo.db.sensor
    output = []
    for q in sensors.find({"Device" : "dev_2"}):
        output.append({'Generate Time' : q['TIMESTAMP'],'Gateway' : q['Gateway'],'Device' : q['Device'], 'Value' : q['value']})
    return jsonify({'result' : output})

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
