import logging
from services.minidsp.handlers import audio

logger = logging.getLogger(__name__)

def process_message(client, topic, payload):
    action = payload['action']
    value = int(payload['value'])

    if action == "set_volume":
        return audio.set_volume(value)
    elif action == 'mute':
        return audio.set_mute(value)
    elif action == 'pause':
        return audio.set_pause(value)
    elif action == 'next':
        return audio.next()
    elif action == 'previous':
        return audio.previous()
    else:
        logger.error(f"Unknown action: {payload}")

    return f'OK {payload["action"]} {payload["value"]}'



