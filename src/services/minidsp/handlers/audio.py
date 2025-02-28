import subprocess
import logging
from pynput.keyboard import Controller, Key

logger = logging.getLogger(__name__)

ZERO_VOLUME = -70
keyboard = None

def set_volume(volume_percent):
    gain = round(ZERO_VOLUME * (100 - volume_percent) / 100)
    command = f'minidsp gain -- {gain}'
    result = subprocess.run(command.split(),capture_output=True, text=True)
    return result


def set_mute(value):
    pass

def set_pause(value):
    global keyboard
    if keyboard is None:
        keyboard = Controller()

    keyboard.press(Key.media_play_pause)
    keyboard.release(Key.media_play_pause)

def next():
    global keyboard
    if keyboard is None:
        keyboard = Controller()

    keyboard.press(Key.media_next)
    keyboard.release(Key.media_next)
    pass

def previous():
    global keyboard
    if keyboard is None:
        keyboard = Controller()

    keyboard.press(Key.media_previous)
    keyboard.release(Key.media_previos)

