import thread
import threading
import paho.mqtt.client as mqtt
from voiceid.sr import Voiceid
from voiceid.db import GMMVoiceDB

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("ais/recognize/request/+")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    thread.start_new_thread(recognize, (msg.payload, ))

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
        label = clusters.keys()[0]
        cluster = voice.get_cluster(label)
        speaker = cluster.get_best_speaker()
        if speaker == "unknown":
            print "need name"
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
