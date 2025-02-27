from common import wifi
from common import mqtt

wifi.connect()
mqtt.publish('/iot/device/test','Connection test')
