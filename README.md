## Introduction
Recognize Speakers and Publish Results

## Messages Structure
| messages           |                          topic         |        payload    |
|:-------------------|:---------------------------------------|:------------------|
| recognize          | ais/recognize/voice/+device_id         | bytes of voice    |
| set name           | ais/recognize/setname/+device_id       | "audio_path=name" |
| recognition result | ais/recognize/result/+device_id/+audio_path  | "speaker_name"    |
| voice unknown      | ais/recognize/unknown/+device_id | "audio_path"      |

## Tasks
- [x] surgemq based MQTT broker
- [x] test publish/subscribe message
- [x] recognition in new thread with voice file specified in message payload
- [x] train speakers model with given voice
- [x] test recognition of trained model
- [x] voice transfer by mqtt payload?(try..)
    - [x] receive bytearray(sent by mock-speaker), save to file
    - [x] pass the file to GStreamer(restricted by the implementation of voiceid)
    - [x] receive bytearray sent from iOS client
- [x] rewrite the method to add/modify voice model! 
    - [x] merge voice models of single speaker
- [x] post to server
- [ ] handle name whitespace
- [ ] message retain

## References
* voiceid: https://code.google.com/p/voiceid/
* MQTT client paho: https://eclipse.org/paho/clients/python/
* MQTT broker surgemq: https://github.com/surgemq/surgemq
* Audio format restricted by: https://developer.apple.com/library/mac/documentation/MusicAudio/Reference/CAFSpec/CAF_spec/CAF_spec.html and http://gstreamer.freedesktop.org/data/doc/gstreamer/head/pwg/html/section-types-definitions.html
* MQTT protocol: http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html
* some manual tests using: http://mqttfx.jfx4ee.org/ 