import paho.mqtt.client as mqtt

def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("ais/recognize/result/#")
    client.publish("ais/recognize/voice/mock-speaker", "")

def on_message(client, userdata, msg):
    print msg.topic + " " + str(msg.payload)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# client.connect("127.0.0.1", 1883, 60)
client.connect("iot.eclipse.org", 1883, 60)

# https://eclipse.org/paho/clients/python/docs/#network-loop
client.loop_forever()