import paho.mqtt.client as mqtt
import json
import handlers
from logger import logger
from paho.mqtt.enums import CallbackAPIVersion
from paho.mqtt.reasoncodes import ReasonCode

def on_connect(client: mqtt.Client, userdata, flags, reason_code: ReasonCode, properties):
    if reason_code.is_failure:
        logger.error(f"Failed to connect: {reason_code}")
    else:
        logger.info("Connected to MQTT Broker!")
        client.subscribe(config["topic"])


def on_message(client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
    logger.debug(f"Received message on {msg.topic}: {msg.payload.decode()}")
    payload = msg.payload.decode()
    handlers.process_message(client, msg.topic, json.loads(payload))


def on_disconnect(client, userdata, disconnect_flags, reason_code, properties):
    logger.info(f"Disconnected: {reason_code}")


with open("config_private.json") as f:
    config = json.load(f)["mqtt"]

with open("/etc/machine-id", "r") as f:
    machine_id = f.read().strip()
print(machine_id)

server_config = min(config["servers"], key=lambda x: x["priority"])
client_id = server_config["client_id"]+machine_id

logger.debug(f'client_id {client_id} user {server_config["user"]} password {server_config["password"]}')

client = mqtt.Client(client_id=client_id,callback_api_version=CallbackAPIVersion.VERSION2)
client.username_pw_set(server_config["user"],server_config["password"])
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

client.connect(server_config["server"], 1883)
client.loop_forever()

