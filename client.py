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

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    print(str(msg.payload))
def on_disconnect(client,userdata,flags,rc=0):
    print("Disconnectred result code "+str(rc))
    
file = open("mac.txt","r")
path = 'ecem119/2018s/hexiwear/'
one = path + file.readline().rstrip('\n')
two = path + file.readline().rstrip('\n')
file.close()

topic1=one
topic2=two
broker="broker.hivemq.com"
client = mqtt.Client("RaspberryM119 Pi2")

client.on_connect = on_connect
client.on_disconnect=on_disconnect
#client.on_message = on_message
#if (connected==0):
print("Conecting to broker ",broker)
client.connect(broker, 1883, 60)

#client.loop_start()
client.subscribe(topic1)
client.subscribe(topic2)
client.on_message = on_message
#client.publish(topic1,"Topic1 message")
#client.publish(topic2,"Topic2 message")
#time.sleep(4)
#client.loop_stop()
#client.disconnect()
client.loop_forever()
