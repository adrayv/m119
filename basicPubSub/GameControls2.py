from bluepy import btle
from bluepy.btle import Scanner, DefaultDelegate, ScanEntry, Peripheral
import struct
import urllib2

import boto3
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse

#~~~~~~~~~AWS IoT API Definitions~~~~~~~~~~~~~~~

# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

# Read in command-line parameters
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--endpoint", action="store", required=True, dest="host", help="Your AWS IoT custom endpoint")
parser.add_argument("-r", "--rootCA", action="store", required=True, dest="rootCAPath", help="Root CA file path")
parser.add_argument("-C", "--CognitoIdentityPoolID", action="store", required=True, dest="cognitoIdentityPoolID",
                    help="Your AWS Cognito Identity Pool ID")
parser.add_argument("-id", "--clientId", action="store", dest="clientId", default="basicPubSub_CognitoSTS",
                    help="Targeted client id")
parser.add_argument("-t", "--topic", action="store", dest="topic", default="sdk/test/Python", help="Targeted topic")

args = parser.parse_args()
host = args.host
rootCAPath = args.rootCAPath
clientId = args.clientId
cognitoIdentityPoolID = args.cognitoIdentityPoolID
topic = args.topic

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Cognito auth
identityPoolID = cognitoIdentityPoolID
region = host.split('.')[2]
cognitoIdentityClient = boto3.client('cognito-identity', region_name=region)
# identityPoolInfo = cognitoIdentityClient.describe_identity_pool(IdentityPoolId=identityPoolID)
# print identityPoolInfo

temporaryIdentityId = cognitoIdentityClient.get_id(IdentityPoolId=identityPoolID)
identityID = temporaryIdentityId["IdentityId"]

temporaryCredentials = cognitoIdentityClient.get_credentials_for_identity(IdentityId=identityID)
AccessKeyId = temporaryCredentials["Credentials"]["AccessKeyId"]
SecretKey = temporaryCredentials["Credentials"]["SecretKey"]
SessionToken = temporaryCredentials["Credentials"]["SessionToken"]

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId, useWebsocket=True)

# AWSIoTMQTTClient configuration
myAWSIoTMQTTClient.configureEndpoint(host, 443)
myAWSIoTMQTTClient.configureCredentials(rootCAPath)
myAWSIoTMQTTClient.configureIAMCredentials(AccessKeyId, SecretKey, SessionToken)
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
time.sleep(2)


# The callback for when a PUBLISH message is received from the server.
def button_publish(button, mac):
    if button==0:
        urllib2.urlopen("https://sheltered-brook-80388.herokuapp.com/update?player=2&action=right").read()
        motion="right"
        messageSent="event "+motion + " @ " + hexi_addr
        myAWSIoTMQTTClient.publish(topic,messageSent,1)
    if button==1:
        urllib2.urlopen("https://sheltered-brook-80388.herokuapp.com/update?player=2&action=left").read()
        motion="left"
        messageSent="event "+motion + " @ " + hexi_addr
        myAWSIoTMQTTClient.publish(topic,messageSent,1)
    if button==2:
        urllib2.urlopen("https://sheltered-brook-80388.herokuapp.com/update?player=2&action=up").read()
        motion="up"
        messageSent="event "+motion + " @ " + hexi_addr
        myAWSIoTMQTTClient.publish(topic,messageSent,1)    
    if button==3:
        urllib2.urlopen("https://sheltered-brook-80388.herokuapp.com/update?player=2&action=down").read()
        motion="down"
        messageSent="event "+motion + " @ " + hexi_addr
        myAWSIoTMQTTClient.publish(topic,messageSent,1)
    if button==4:
        urllib2.urlopen("https://sheltered-brook-80388.herokuapp.com/update?player=2&action=buzz").read()
        motion="HandRaised"
        messageSent="event "+motion + " @ " + hexi_addr
        myAWSIoTMQTTClient.publish(topic,messageSent,1)


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
