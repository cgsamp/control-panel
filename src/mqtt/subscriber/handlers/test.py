import logging
logger = logging.getLogger(__name__)

def process_message(client, topic, payload):
    logger.debug(payload)
    action = payload["action"]
    logger.debug(f'Processing {action}')

    if action == 'ping':
        ping(payload)
    else:
        logger.error(f"Unknown action: {payload}")

def ping(payload):
    logger.debug(f'Ping {payload}')

