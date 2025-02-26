JSON_PAYLOAD='{
  "action": "set_volume",
  "value": 50,
  "device_id": "speaker_1"
}'

mosquitto_pub -d -r \
-u samp_device \
-P Device2@ \
-i samp_mosquito_pub \
-h studio.lab.sampsoftware.net \
-t  /iot/controls/audio \
-m "$JSON_PAYLOAD"
