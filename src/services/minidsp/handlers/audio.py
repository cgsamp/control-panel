import subprocess
from common.logger import logger

ZERO_VOLUME = -70

def set_volume(volume_percent):
    logger.debug(f'Setting volume to {volume_percent}%')

    gain = round(ZERO_VOLUME * (100 - volume_percent) / 100)
    command = f'minidsp gain -- {gain}'
    logger.debug(f'Setting volume to {volume_percent}% gain {gain} command {command}')

    result = subprocess.run(command.split(),capture_output=True, text=True)
    logger.debug(result)


def mute(value):
    if value:
        logger.debug('Muting')
    else:
        logger.debug('Unmuting')

#set_volume(100)
