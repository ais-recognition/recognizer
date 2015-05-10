import thread
import os
import threading
import shutil
import requests
import json
import paho.mqtt.client as mqtt
from voiceid import fm
from voiceid.sr import Voiceid
from voiceid.sr import Cluster
from voiceid.db import GMMVoiceDB

NEW_VOICE_TOPIC = "ais/recognize/voice/+"
SET_NAME_TOPIC = "ais/recognize/setname/+"
HEADERS = {'Content-Type': 'application/json'}

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(NEW_VOICE_TOPIC)
    client.subscribe(SET_NAME_TOPIC)
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print msg.topic
    # print msg.payload

    device_id = msg.topic.split("/")[-1]
    if device_id == "test_id":
        return
    if mqtt.topic_matches_sub(NEW_VOICE_TOPIC, msg.topic):
        file_name = str(msg.timestamp) + '.m4a'
        new_voice = open(file_name, 'wb')
        new_voice.write(msg.payload)
        new_voice.close()
        # payload is less than 256M
        # payload is bytearray or string: http://git.eclipse.org/c/paho/org.eclipse.paho.mqtt.python.git/tree/src/paho/mqtt/client.py
        thread.start_new_thread(recognize, (device_id, file_name))

    elif mqtt.topic_matches_sub(SET_NAME_TOPIC, msg.topic):
        path_and_name = msg.payload.split("=", 1)
        if len(path_and_name) < 2:
            client.publish("ais/recognize/err", "name")
            return
        voice_path = path_and_name[0]
        name = path_and_name[1]
        thread.start_new_thread(set_name, (device_id, voice_path, name))

def set_name(device_id, voice_path, new_name):
    print "set " + voice_path + " to: " + new_name
    new_name = new_name.replace(' ', '')
    if not new_name.isalnum():
        print 'error: SPEAKER_ID must be alphanumeric'
        return
    if new_name in db.get_speakers()['U'] or new_name in db.get_speakers()['M'] or new_name in db.get_speakers()['F']:
        voice = Voiceid(db, voice_path, single=True)
        voice.extract_speakers(quiet=True, thrd_n=3)

        cluster = voice.get_cluster('S0')
        cluster.set_speaker(new_name)
        voice.update_db()
        return
    try:
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
    except TypeError:
        print "Type error"

def recognize(device_id, voice_path):
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
        # speaker = cluster.get_best_speaker()
        speaker = "unknown"
        speakers = cluster.get_best_five()
        if len(speakers) > 0:
            value = speakers[0][1]
            if value > -33.0:
                speaker = speakers[0][0]
        # speaker = cluster.get_speaker()

        print speaker
        payload = {'audio': 'http://52.24.205.33/voice/' + voice_path, 'userName': speaker}
        requests.post('http://129.236.234.21:8080/message', data=json.dumps(payload), headers=HEADERS)
        client.publish("ais/recognize/result/" + device_id + "/" + voice_path, speaker)
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
