import paho.mqtt.client as mqtt_client
import json
from common.logger import logger
from paho.mqtt.enums import CallbackAPIVersion
from paho.mqtt.reasoncodes import ReasonCode
from mqtt.subscriber.handlers import audio
from mqtt.subscriber.handlers import test
import argparse
import fnmatch
from json.decoder import JSONDecodeError
import base64


handler_list = [
    ('*audio*', audio.process_message),
    ('*test*', test.process_message)
]
handle_default = test.process_message

def get_handler(topic):
    """Find the first matching handler for a topic."""
    for pattern, handler in handler_list:
        if fnmatch.fnmatch(topic, pattern):
            return handler
    return handle_default


def on_connect(client: mqtt_client.Client, userdata, flags, reason_code: ReasonCode, properties):
    if reason_code.is_failure:
        logger.error(f"Failed to connect: {reason_code}")
    else:
        logger.info("Connected to MQTT Broker!")


def on_message(client: mqtt_client.Client, userdata, msg: mqtt_client.MQTTMessage):
    logger.debug(f"Received message on {msg.topic}: {msg.payload.decode()}")
    topic = msg.topic
    payload = None

    try:
        payload = json.loads(msg.payload.decode())
    except JSONDecodeError:
        logger.debug(f'Not json payload, wrapping')
        payload = {
            "action" : "raw",
            "data": payload
        }

    handler = get_handler(topic)
    logger.debug(handler)
    handler(client,topic,payload)


def on_disconnect(client, userdata, disconnect_flags, reason_code, properties):
    logger.info(f"Disconnected: {reason_code}")


def setup_client(topic):
    with open("mqtt/subscriber/config_private.json") as f:
        config = json.load(f)["mqtt"]

    with open("/etc/machine-id", "r") as f:
        machine_id = f.read().strip()
    print(machine_id)

    server_config = min(config["servers"], key=lambda x: x["priority"])
    client_id = server_config["client_id"]+machine_id

    logger.debug(f'client_id {client_id} user {server_config["user"]} password {server_config["password"]}')

    client = mqtt_client.Client(client_id=client_id,callback_api_version=CallbackAPIVersion.VERSION2)
    client.username_pw_set(server_config["user"],server_config["password"])
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.connect(server_config["server"], 1883)

    if topic is None:
        topic = config['topic']

    logger.info(f'Subscribing to topic {topic}')
    client.subscribe(topic, qos=0)
    return client


def setup_arg_parser():
    parser = argparse.ArgumentParser(description="Key-Value switch example")
    parser.add_argument("--topic", "-t", type=str, help="Specify topic, overriding config")
    return parser


parser = setup_arg_parser()
args = parser.parse_args()

client = setup_client(args.topic)
client.loop_forever()

