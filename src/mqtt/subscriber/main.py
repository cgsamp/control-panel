import json
import argparse
import fnmatch
import logging
from json.decoder import JSONDecodeError

import paho.mqtt.client as mqtt_client
from paho.mqtt.enums import CallbackAPIVersion
from paho.mqtt.reasoncodes import ReasonCode

from mqtt.subscriber.handlers import audio_subscriber
from mqtt.subscriber.handlers import test

logger = logging.getLogger(__name__)


handler_list = [
    ('*audio*', audio_subscriber.process_message),
    ('*test*', test.process_message)
]
handle_default = test.process_message

def get_handler(topic):
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
    logger.debug(f'Received call on topic {msg.topic}')
    logger.trace(f"Received {msg.topic}: {msg.payload.decode()}")
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
    result = handler(client,topic,payload)
    logger.debug(result)


def on_disconnect(client, userdata, disconnect_flags, reason_code, properties):
    logger.info(f"Disconnected: {reason_code}")


def setup_client(topic):
    with open("mqtt/subscriber/config_private.json") as f:
        config = json.load(f)["mqtt"]
    server_config = min(config["servers"], key=lambda x: x["priority"])

    with open("/etc/machine-id", "r") as f:
        machine_id = f.read().strip()
    client_id = server_config["client_id"]+machine_id

    if topic is None:
        topic = config['topic']

    logger.debug(f'client_id={client_id} user={server_config["user"]} p_len={len(server_config["password"])} topic={topic}')

    client = mqtt_client.Client(client_id=client_id,callback_api_version=CallbackAPIVersion.VERSION2)
    client.username_pw_set(server_config["user"],server_config["password"])
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.connect(server_config["server"], 1883)
    client.subscribe(topic, qos=0)

    return client


def get_args():
    parser = argparse.ArgumentParser(description="Subscriber config")
    parser.add_argument("--topic", "-t", type=str, help="Specify topic, overriding config")
    return parser.parse_args()


args = get_args()
client = setup_client(args.topic)
client.loop_forever()

