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

print("Conecting to broker ",broker)
client.connect(broker, 1883, 60)

client.loop_start()
#client.subscribe(topic1)
#client.subscribe(topic2)
#client.publish(topic1,"Topic1 message")
#client.publish(topic2,"Topic2 message")
button_publish(0,"MACTEST")
#time.sleep(4)
client.loop_stop()
client.disconnect()
