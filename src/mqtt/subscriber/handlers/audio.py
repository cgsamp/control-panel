import time
from common.logger import logger
from services.minidsp.handlers import audio

def process_message(client, topic, payload):
    action = payload["action"]
    logger.debug(f'Processing {action}')

    if action == "set_volume":
        set_volume(payload)
    else:
        logger.error(f"Unknown action: {payload}")

def set_volume(payload):
    volume = int(payload['value'])
    logger.debug(f'ADJUSTING VOUME to {volume}')
    audio.set_volume(volume)

