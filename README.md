# RecognitionBroker
Recognize Speakers and Publish Results

## Messages Structure
| messages           |                          topic         |        payload    |
|:-------------------|:---------------------------------------|:------------------|
| recognize          | ais/recognize/voice/+device_id         | bytes of voice    |
| set name           | ais/recognize/setname/+device_id       | "audio_path=name" |
| recognition result | ais/recognize/voice/result/+device_id  | "speaker_name"    |
| voice unknown      | ais/recognize/voice/unknown/+device_id | "audio_path"      |

## Tasks
- [x] surgemq based MQTT broker
- [x] test publish/subscribe message
- [x] recognition in new thread with voice file specified in message payload
- [x] train speakers model with given voice
- [x] test recognition of trained model
- [ ] voice transfer by mqtt payload?(try..)
    - [x] receive bytearray(sent by mock-speaker), save to file
    - [x] pass the file to GStreamer(restricted by the implementation of voiceid)
    - [ ] receive bytearray sent from iOS client
- [ ] handle name duplicates
- [ ] handle name whitespace
- [ ] message retain

## References
* voiceid: https://code.google.com/p/voiceid/
* MQTT client paho: https://eclipse.org/paho/clients/python/
* MQTT broker surgemq: https://github.com/surgemq/surgemq
* Audio format restricted by: https://developer.apple.com/library/mac/documentation/MusicAudio/Reference/CAFSpec/CAF_spec/CAF_spec.html and http://gstreamer.freedesktop.org/data/doc/gstreamer/head/pwg/html/section-types-definitions.html
* MQTT protocol: http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html
* some manual tests using: http://mqttfx.jfx4ee.org/ 