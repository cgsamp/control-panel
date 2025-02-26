import time
from logger import logger

def process_message(client, topic, payload):
    logger.debug(payload)
    action = payload["action"]
    logger.debug(f'Processing {action}')

    if action == "set_volume":
        set_volume(payload)
    else:
        logger.error(f"Unknown action: {payload}")

def set_volume(payload):
    logger.debug(f'ADJUSTING VOUME')

