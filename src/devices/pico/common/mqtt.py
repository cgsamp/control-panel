from umqtt.robust import MQTTClient
from common import helps

_client = None
_connected = False

def _create_client():
    config = helps.get_config("mqtt")
    server_config = min(config["servers"], key=lambda x: x["priority"])
    client_id = server_config["client_id"]+helps.get_machine_id()
    _client = MQTTClient(
                    client_id,
                    server_config["server"],
                    user=server_config["user"],
                    password=server_config["password"]
                )

def publish_raw(topic, message, keepalive=True):
    if _client is None:
        helps.log(helps.LOG_DEBUG,f'Creating client')
        _create_client()
    
    if not _connected:
        helps.log(helps.LOG_DEBUG,f'Connecting...')
        _client.connect()
        _connected = True

    helps.log(helps.LOG_DEBUG,f'Publishing {topic} {message}')
    _client.publish(
        topic,
        message
        )
    
    if not keepalive:
        helps.log(helps.LOG_DEBUG,f'Disconnecting.')
        _client.disconnect()
        _connected = False
        
def publish_action(topic,action,value,keepalive=True):
    structured_message = []
    structured_message['action'] = action
    structured_message['value'] = value
    structured_message['machine_id'] = helps.get_machine_id()
    structured_message['time_micros'] = helps.ts()
    structured_message['timestamp'] = helps.ts_formatted()
    publish_raw(topic,json.dumps(structured_message),keepalive)

