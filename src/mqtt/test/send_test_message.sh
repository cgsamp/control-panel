JSON_PAYLOAD='{
  "action": "set_volume",
  "value": 100,
  "device_id": "speaker_1"
}'

JSON_PAYLOAD='{
  "action": "pause",
  "value": 1
}'

#TOPIC='/iot/device/test'
#TOPIC='lab/test-device'
TOPIC='/iot/controls/audio'

mosquitto_pub -d \
-u samp_device \
-P Device2@ \
-i samp_mosquito_pub \
-h studio.lab.sampsoftware.net \
-t  "$TOPIC" \
-m "$JSON_PAYLOAD"
