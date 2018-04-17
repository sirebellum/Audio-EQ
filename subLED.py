# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO

import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
# Subscribing in on_connect() means that if we lose the connection and
# reconnect then subscriptions will be renewed.
    client.subscribe("test/led")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print "Topic: ", msg.topic+'\nMessage: '+str(msg.payload)
    if msg.payload.decode() == "ENGAGE":
        GPIO.output(18,GPIO.HIGH)
        GPIO.output(10,GPIO.LOW)

    if msg.payload.decode() == "DISENGAGE":
        GPIO.output(18,GPIO.LOW)
        GPIO.output(10,GPIO.HIGH)
    #client.disconnect()

############ MAIN ###############
# Sets naming convention for pins
GPIO.setmode(GPIO.BCM)

# Prevent warnings from printing, who needs 'em!
GPIO.setwarnings(False)

# Set GPIO pins as outputs
GPIO.setup(18,GPIO.OUT)
GPIO.setup(10,GPIO.OUT)

# Set up MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# BrokerIP, Mosquitto port 1883: unencrypted
client.connect("192.168.1.14", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
