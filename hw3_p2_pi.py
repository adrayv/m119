from bluepy import btle
from bluepy.btle import Scanner, DefaultDelegate, ScanEntry, Peripheral
import struct

import paho.mqtt.client as mqtt
import time
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("Connected with result code "+str(rc))
    else:
        print("Bad Connection. Returned Code=",rc)
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

file = open("mac.txt","r")
path = 'ecem119/2018s/hexiwear/'
one = path + file.readline().rstrip('\n')
two = path + file.readline().rstrip('\n')
file.close()

topic1=one
topic2=two
broker="broker.hivemq.com"
client = mqtt.Client("RaspberryM119 Pi1")
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    print(str(msg.payload))

def on_disconnect(client,userdata,flags,rc=0):
    print("Disconnectred result code "+str(rc))
    
def button_publish(button, mac):
    if button==0:
        motion="right"
        messageSent="event "+motion+" @ "+ mac
        client.publish(topic1,messageSent)
    if button==1:
        motion="left"
        messageSent="event "+motion+" @ "+ mac
        client.publish(topic1,messageSent)
    if button==2:
        motion="up"
        messageSent="event "+motion+" @ "+ mac
        client.publish(topic1,messageSent)    
    if button==3:
        motion="down"
        messageSent="event "+motion+" @ "+ mac
        client.publish(topic1,messageSent)

client.on_connect = on_connect
client.on_disconnect=on_disconnect
client.on_message = on_message
client.connect(broker, 1883, 60)

hexi_addr = None

# This is a delegate for receiving BTLE events
class BTEventHandler(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
    	# Advertisement Data
        if isNewDev:
            print "Found new device:", dev.addr, dev.getScanData()

        # Scan Response
        if isNewData:
            print "Received more data", dev.addr, dev.getScanData()

    def handleNotification(self, cHandle, data):
    	# Only print the value when the handle is 40 (the battery characteristic)
        if cHandle == 40:
            buttonPressed = struct.unpack('B', data)[0]
            print buttonPressed
            button_publish(buttonPressed,hexi_addr)
            
handler = BTEventHandler()

# Create a scanner with the handler as delegate
scanner = Scanner().withDelegate(handler)

# Start scanning. While scanning, handleDiscovery will be called whenever a new device or new data is found
devs = scanner.scan(10.0)

# Get HEXIWEAR's address
hexi_addr = [dev for dev in devs if dev.getValueText(0x8) == 'HEXIWEAR'][0].addr
# hexi_addr = '00:2A:40:08:00:10'

# Create a Peripheral object with the delegate
hexi = Peripheral().withDelegate(handler)

# Connect to Hexiwear
hexi.connect(hexi_addr)

# Get the battery service
battery = hexi.getCharacteristics(uuid="2a19")[0]
# battery = hexi.getCharacteristics(uuid="2001")[0]

# Get the client configuration descriptor and write 1 to it to enable notification
battery_desc = battery.getDescriptors(forUUID=0x2902)[0]
# battery_desc = battery.getDescriptors(forUUID=0x2001)[0]
battery_desc.write(b"\x01", True)

# Infinite loop to receive notifications
while True:
    hexi.waitForNotifications(1.0)
