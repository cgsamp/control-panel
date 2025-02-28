import micropython
import time
import json
from time import sleep
from machine import Pin, I2C
from controls.audio_controls import AudioControl, Potentiometer, Switch, Rotary, Display
from common import helps
from common import mqtt

class ControlPanel():
    def __init__(self):
        helps.log(helps.LOG_DEBUG,'Init control panel')
        config = helps.get_config('control_panel')
    
        self._inputs = []

        for item_config in config["inputs"]:
            if item_config["type"] == "potentiometer":
                self._inputs.append(Potentiometer(item_config))
            elif item_config["type"] == "switch":
                self._inputs.append(Switch(item_config))
            elif item_config["type"] == "rotary":
                self._inputs.append(Rotary(item_config))
            else:
                raise NotImplementedError(f"{item_config}")
                
        helps.log_debug(self._inputs)
        self._outputs = []
        self._display = None

        for item_config in config["outputs"]:
            if item_config["type"] == "display":
                self._display = Display(item_config)
                #outputs.append(Display(item_config))
            else:
                NotImplementedError(f"{item_config}")

        self._idle_timeout = 5 * 1000

    def loop_forever(self):
        helps.log(helps.LOG_DEBUG,'Control panel loop')
        first_loop = True
        last_updated = time.ticks_ms()

        while True:
            try:
                if time.ticks_ms() - last_updated > self._idle_timeout:
                    self._display.idle = True
                for input in self._inputs:
                    value, changed = input.get_current_value()
                    if changed:
                        if not first_loop:
                            self._dispatch_action(input.get_id(),input.get_display_name(),value)
                        self._display.idle = False                    
                        last_updated = time.ticks_ms()
                first_loop = False
                sleep(0.01)
                            
            except KeyboardInterrupt:
                self._display.on = False
                break

    def _dispatch_action(self,id,display_name,value):
        self._display.show_control_status(id, value)
        helps.log_debug(f'{id}:{display_name} = {value}')
        if id == 1:
            mqtt.publish_action('/iot/controls/audio','set_volume',value)

            
            
            