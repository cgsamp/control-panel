from umqtt.robust import MQTTClient
import machine

import network
import json
import time

with open("config_connections.json") as f:
    config = json.load(f)["mqtt"]

server_config = min(config["servers"], key=lambda x: x["priority"])


client_id = server_config["client_id"]+str(machine.unique_id().hex())

mqtt_client = MQTTClient(
                client_id,
                server_config["server"],
                user=server_config["user"],
                password=server_config["password"]
            )

mqtt_client.connect()


t = time.localtime()
timestamp = "{:04}-{:02}-{:02};{:02}:{:02}:{:02}.{:06}".format(
    t[0], t[1], t[2], t[3], t[4], t[5], int(time.ticks_ms())
)

message = f'Test from {client_id} at {timestamp}'

mqtt_client.publish(
    '/lab/test/ping',
    message
    )