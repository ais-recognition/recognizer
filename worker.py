import paho.mqtt.client as mqtt
from voiceid.sr import Voiceid
from voiceid.db import GMMVoiceDB

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("ssss/")
	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
db = GMMVoiceDB('voiceDB')
db.add_model('yuannancai_wav', 'Yuannan Cai')
db.add_model('yuzhongji_wav', 'Yuzhong Ji')
print db.get_speakers()

v = Voiceid(db, 'cyn.m4a')
v.extract_speakers()
label = v.get_clusters()[0]
cluster = v.get_cluster(label)
print cluster

client.connect("127.0.0.1", 1883, 60)
# client.connect("iot.eclipse.org", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
