#!/usr/bin/env pybricks-micropython
#This is a bi-directional communication between an EV3 Brick client with an MQTT Client (MQTTX)
import time
import json
from umqtt.simple import MQTTClient
import machine
import ubinascii

#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port

# Setup a GPIO Pin for output
ev3 = EV3Brick()

# Setup the motor to run in a counterclockwise direction
motor = Motor(Port.C,Direction.COUNTERCLOCKWISE)
motor2 = Motor(Port.B,Direction.CLOCKWISE)

state = False

# Modify below section as required
CONFIG = {
    # Configuration details of the MQTT broker
    "MQTT_BROKER": "broker.emqx.io",
    "USER": "",
    "PASSWORD": "",
    "PORT": 1883,
    "TOPIC": b"motor_speed",
    # unique identifier of the chip
    "CLIENT_ID": b"EV3BRICK" + ubinascii.hexlify(machine.unique_id())
}

#GLOBAL VARIABLES IN SCOPE
client = MQTTClient(CONFIG['CLIENT_ID'], CONFIG['MQTT_BROKER'], user=CONFIG['USER'], password=CONFIG['PASSWORD'], port=CONFIG['PORT'])
state = False 

def runMotor(speed):
    print("speed is %s" %speed)
    global state
    print(state)
    
    while state:
        motor.run(speed)
        motor2.run(speed)
        time.sleep(1)
        print(state)
        client.check_msg()
    print("Motor Stopped running")
                              
# Method to act based on message received   
def onMessage(topic, msg):
    print("OnMessage called")
    global state
    if (state == False):
        state = not state
    print("The state is : ")
    print(state)
    print("Topic: %s, Message: %s" % (topic, msg))
    stringMessage = msg.decode()
    speed = int(stringMessage)
    if(topic == b'motor_speed'):
        runMotor(speed)
    
def listen():
    client.set_callback(onMessage)
    client.connect()
    client.publish("test", "EV3 Brick is Connected")
    client.subscribe(CONFIG['TOPIC'])
    print("EV3 Brick is Connected to %s and subscribed to %s topic" % (CONFIG['MQTT_BROKER'], CONFIG['TOPIC']))

    try:
        while True:
            msg = client.wait_msg()
            
            print("The return message: ")
            print(msg)
            
    finally:
        client.disconnect()  

listen()


