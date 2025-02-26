import micropython
import time
import json
from time import sleep
from machine import Pin, I2C
from audio_controls import Potentiometer
from audio_controls import Switch
from audio_controls import RotaryInterrupt
from audio_controls import Display


with open("config.json") as f:
    config = json.load(f)

pots = []

for item in config["inputs"]["potentiometers"]:
    pots.append(Potentiometer(config=item))

switches = []

for item in config["inputs"]["switches"]:
    switches.append(Switch(config=item))

rotaries = []

for item in config["inputs"]["rotary_encoders"]:
    print(item)
    rotaries.append(RotaryInterrupt(config=item))

# Create the I2C interface.
#i2c = I2C(sda=TP_SDA, scl=TP_SCL, freq=400000)

#i2c = I2C(freq=400000)          # create I2C peripheral at frequency of 400kHz
                                # depending on the port, extra parameters may be required
                                # to select the peripheral and/or pins to use

#print(f'scans={i2c.scan()}')



#i2c.writeto(42, b'123')         # write 3 bytes to peripheral with 7-bit address 42
#i2c.readfrom(42, 4)             # read 4 bytes from peripheral with 7-bit address 42

#i2c.readfrom_mem(42, 8, 3)      # read 3 bytes from memory of peripheral 42,
                                #   starting at memory-address 8 in the peripheral
#i2c.writeto_mem(42, 2, b'\x10') # write 1 byte to memory of peripheral 42
                                #   starting at address 2 in the peripheral




while True:
    for item in pots:
        print(f'Name: {item.get_display_name():15}, Value: {item.get_current_value()[0]:03d}', end=" ")
    for item in switches:
        print(f'Name: {item.get_display_name():15}, Value: {item.get_current_value()[0]:03d}', end=" ")
    for item in rotaries:
        print(f'Name: {item.get_display_name():15}, Value: {item.get_current_value()[0]:03d}', end=" ")
    print()
    sleep(0.2)
 
 
 
 
    