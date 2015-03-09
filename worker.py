import thread
import os
import threading
import shutil
import paho.mqtt.client as mqtt
from voiceid import fm
from voiceid.sr import Voiceid
from voiceid.sr import Cluster
from voiceid.db import GMMVoiceDB

NEW_VOICE_TOPIC = "ais/recognize/voice"
SET_NAME_TOPIC = "ais/recognize/setname/#"
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
        voice_path = msg.topic.split("/")[-1]
        thread.start_new_thread(set_name, (voice_path, msg.payload))

def set_name(voice_path, new_name):
    print "set " + voice_path + " to: " + new_name
    try:
        # voice = Voiceid(db, voice_path, single=True)
        # voice.extract_speakers(thrd_n=5)
        # cluster = voice.get_cluster('S0')
        # cluster.set_speaker(new_name)
        # voice.update_db()
        # To Do: replace whitespace to path special character
        if not new_name.isalnum():
            print 'error: SPEAKER_ID must be alphanumeric'
            exit(1)
        # assume only one speaker in one sample
        ww = fm.file2wav(voice_path)
        file_basename, extension = os.path.splitext(ww)
        db.add_model(file_basename, new_name)
        os.remove(file_basename + ".seg")
        os.remove(file_basename + ".ident.seg")
        os.remove(file_basename + ".init.gmm")
    except IOError:
        print "voice file doesn't exist"
    except OSError:
        print "WARNING: error deleting some intermediate files"

def recognize(voice_path):
    # voice_db_lock.acquire()
    print db.get_speakers()
    # assume only one speaker in one sample, To Do: multiple speakers in one sample
    # set to True to force to avoid diarization, in case a single speaker in the file
    try:
        voice = Voiceid(db, voice_path, single=True)
        # extract_speakers(interactive=False, quiet=False, thrd_n=1)
        voice.extract_speakers(quiet=True, thrd_n=3)
        # clusters = voice.get_clusters()
        cluster = voice.get_cluster('S0')
        speaker = cluster.get_best_speaker()
        # speaker = cluster.get_speaker()
        if speaker == "unknown":
            print "need name"
            client.publish("ais/recognize/unknown", voice_path)
        else:
            print speaker
        os.remove(voice.get_file_basename() + '.seg')
        os.remove(voice.get_file_basename() + '.g.seg')
        os.remove(voice.get_file_basename() + '.s.seg')
        w = voice.get_file_basename() + '.wav'
        if voice.get_filename() != w:
            os.remove(w)
        shutil.rmtree(voice.get_file_basename())
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
