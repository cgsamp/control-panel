from machine import Pin, ADC, I2C
from rotary.rotary_irq_rp2 import RotaryIRQ
from hybotics_ht16k33.segments import Seg7x4
from hybotics_ht16k33 import segments


class AudioControl(object):
    def __init__(self, id, display_name, assignment, location):
        self._id = id
        self._display_name = display_name
        self._assignment = assignment
        self._location = location
        
    def get_location(self):
        return self._location

    def get_id(self):
        return self._id

    def get_current_value(self):
        raise NotImplementedError("AudioControl")
    
    def get_display_name(self):
        return self._display_name
       

class Potentiometer(AudioControl):
    POT_MAX = 65535
    POT_SCALE = 99
    POT_DEBOUNCE = POT_SCALE // 40
    
    def __init__(self, config):
        if config is None:
            raise NotImplementedError("Pot non-json config")
        super().__init__(
            id = config["id"],
            display_name = config["display_name"],
            assignment = config["assignment"],
            location = config["location"]
        )            
            
        self._wiper_pin_number = config["wiper_pin"]
        self._polarity = config["polarity"]
        
        self._wiper = ADC(Pin(self._wiper_pin_number))
        self._current_value = -1
        
    def get_current_value(self):
        changed = False
        raw_value = self._wiper.read_u16()
        new_value = round(raw_value * Potentiometer.POT_SCALE / Potentiometer.POT_MAX)
        if self._polarity == 'reversed':
            new_value = Potentiometer.POT_SCALE - new_value
                 
        if (abs(self._current_value - new_value)) >= Potentiometer.POT_DEBOUNCE:
            self._current_value = new_value
            changed = True
        return self._current_value, changed
    
    
class Switch(AudioControl):
    def __init__(self, config):
        if config is None:
            raise NotImplementedError("Pot non-json config")
        assignment = ""
        if 'assignment' in config:
            assignment = config['assignment']
        super().__init__(
            id = config["id"],
            display_name = config["display_name"],
            assignment = assignment,
            location = config["location"]
        )
        self._pin_number = config["pin"]
        self._pin = Pin(self._pin_number,Pin.IN,Pin.PULL_UP)
        self._current_value = -1

    def get_current_value(self):
        changed = False
        raw_value = self._pin.value()
        if self._current_value != raw_value:
            changed = True
            self._current_value = raw_value
            
        return raw_value, changed
    
    
class Rotary(AudioControl):
    def __init__(self, config):
        if config is None:
            raise NotImplementedError("Pot non-json config")
        assignment = ""
        if 'assignment' in config:
            assignment = config['assignment']
        super().__init__(
            id = config["id"],
            display_name = config["display_name"],
            assignment = assignment,
            location = config["location"]
        )
        self._clk_pin_number = config["pin_a"]
        self._dt_pin_number =  config["pin_b"]
        
        self._rot = RotaryIRQ(pin_num_clk=self._clk_pin_number,
                          pin_num_dt=self._dt_pin_number,
                          min_val=config["bottom_range"],
                          max_val=config["top_range"],
                          pull_up=True,
                          reverse=False,
                          range_mode=RotaryIRQ.RANGE_BOUNDED)

        self._rot.reset()
        self._current_value = self._rot.value()
                               
    def get_current_value(self):
        changed = False
        raw_value = self._rot.value()
        if self._current_value != raw_value:
            changed = True
            self._current_value = raw_value
            
        return raw_value, changed
        
class Display(AudioControl):
    def __init__(self, config):
        if config is None:
            raise NotImplementedError("Pot non-json config")
        if 'assignment' in config:
            assignment = config['assignment']
        super().__init__(
            id = config["id"],
            display_name = config["display_name"],
            assignment = assignment,
            location = config["location"]
        )
        self._scl_pin_number = config["scl_pin"]
        self._sda_pin_number =  config["sca_pin"]
        i2c = I2C(0,sda=self._sda_pin_number,scl=self._scl_pin_number, freq=400000)

        devices = i2c.scan()
        segment_display_address = devices.pop()

        self._display = Seg7x4(i2c)
        self._display.brightness = 0.5
        self._display.colon = True
        self._on = False
        self._display.on = False
        self._idle = False
        self._wake_brightness = self._display.brightness
        

    def show_control_status(self,location,value):
        if self.idle:
            self.idle = False
        print_string = ''
        if location < 10:
            print_string += ' '
        print_string += str(location)
        if value < 10 and value >= 0:
            print_string += ' '
        print_string += str(value)
        self._display.print(print_string)

    @property
    def on(self):
        return self._on

    @on.setter
    def on(self, turn_on):
        if turn_on != self._on:
            self._display.on = turn_on
        

    @property
    def idle(self):
        return self._idle

    @idle.setter
    def idle(self, turn_on):
        if turn_on != self._idle:
            self._idle = turn_on
            if turn_on:
                self._display.brightness = 0.01
                self._display.print('    ')
            else:
                self._display.brightness = self._wake_brightness
        

