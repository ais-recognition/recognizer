import thread
import threading
import paho.mqtt.client as mqtt
from voiceid.sr import Voiceid
from voiceid.sr import Cluster
from voiceid.db import GMMVoiceDB

NEW_VOICE_TOPIC = "ais/recognize/voice"
SET_NAME_TOPIC = "ais/recognize/setname/+"
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(NEW_VOICE_TOPIC)
    client.subscribe(SET_NAME_TOPIC)
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if msg.topic == NEW_VOICE_TOPIC:
        thread.start_new_thread(recognize, (msg.payload, ))
    elif msg.topic.startswith(SET_NAME_TOPIC[0: -1]):
        cluster_label = msg.topic.split("/")[-1]
        thread.start_new_thread(set_name, (cluster_label, msg.payload))

def set_name(cluster_label, new_name):
    print "set " + cluster_label + " to: " + new_name
    cluster = Cluster(cluster_label)
    print cluster
    cluster.set_speaker(new_name)

def recognize(voice_path):
    # voice_db_lock.acquire()
    # db = GMMVoiceDB('voiceDB')
    print db.get_speakers()
    # assume only one speaker in one sample, To Do: multiple speakers in one sample
    # set to True to force to avoid diarization, in case a single speaker in the file
    try:
        voice = Voiceid(db, voice_path, single=True)
        # extract_speakers(interactive=False, quiet=False, thrd_n=1)
        voice.extract_speakers()
        clusters = voice.get_clusters()
        cluster_label = clusters.keys()[0]
        cluster = voice.get_cluster(cluster_label)
        speaker = cluster.get_best_speaker()
        if speaker == "unknown":
            print "need name"
            cluster.set_speaker("unknown")
            voice.update_db()
            client.publish("ais/recognize/unknown", cluster_label)
        else:
            print speaker
    except IOError:
        print "voice file doesn't exist"
        # voice_db_lock.release()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
# set_maxthreads(trd)
db = GMMVoiceDB("voiceDB")

voice_db_lock = threading.Lock()
# client.connect("127.0.0.1", 1883, 60)
client.connect("iot.eclipse.org", 1883, 60)

# https://eclipse.org/paho/clients/python/docs/#network-loop
client.loop_forever()
