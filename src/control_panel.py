import micropython
import time
import json
from time import sleep
from machine import Pin, I2C
from audio_controls import AudioControl
from audio_controls import Potentiometer
from audio_controls import Switch
from audio_controls import Rotary
from audio_controls import Display

with open("config.json") as f:
    config = json.load(f)

inputs = []

for item_config in config["inputs"]:
    if item_config["type"] == "potentiometer":
        inputs.append(Potentiometer(item_config))
    elif item_config["type"] == "switch":
        inputs.append(Switch(item_config))
    elif item_config["type"] == "rotary":
        inputs.append(Rotary(item_config))
    else:
        raise NotImplementedError(f"{item_config}")
        
        
outputs = []
display = None

for item_config in config["outputs"]:
    if item_config["type"] == "display":
        display = Display(item_config)
        #outputs.append(Display(item_config))
    else:
        NotImplementedError(f"{item_config}")


idle_timeout = 5 * 1000
last_updated = time.ticks_ms()
display.on = True
first_loop = True

while True:
    try:
        if time.ticks_ms() - last_updated > idle_timeout:
            display.idle = True
        for input in inputs:
            value, changed = input.get_current_value()
            if changed:
                #print(f'{input.get_display_name()}:{input.get_id()} changed to {value}')
                if not first_loop:
                    display.show_control_status(input.get_id(), value)
                display.idle = False                    
                last_updated = time.ticks_ms()
        first_loop = False
        sleep(0.01)
                    
    except KeyboardInterrupt:
        display.on = False
        break


