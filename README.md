# RecognitionBroker
Recognize Speakers and Publish Results

## To Do
- [x] surgemq based MQTT broker
- [x] test publish/subscribe message
- [x] recognition in new thread with voice file specified in message payload
- [x] train speakers model with given voice
- [x] test recognition of trained model
- [ ] voice transfer by mqtt payload?(try..)
- [ ] handle name duplicates
- [ ] handle name whitespace
- [ ] message retain

## References
* voiceid: https://code.google.com/p/voiceid/
* MQTT client paho: https://eclipse.org/paho/clients/python/
* MQTT broker surgemq: https://github.com/surgemq/surgemq
* support audio format restricted by: https://developer.apple.com/library/mac/documentation/MusicAudio/Reference/CAFSpec/CAF_spec/CAF_spec.html and http://gstreamer.freedesktop.org/data/doc/gstreamer/head/pwg/html/section-types-definitions.html
