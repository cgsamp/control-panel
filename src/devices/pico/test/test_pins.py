from machine import Pin, ADC
from utime import sleep
#from collections import OrderedDict
#import adafruit_ht16k33.segments

def blink():
    pin = Pin("LED", Pin.OUT)

    print("LED starts flashing...")
    while True:
        try:
            pin.toggle()
            sleep(1) # sleep 1sec
        except KeyboardInterrupt:
            break
    pin.off()
    print("Finished.")

pins = []
adcs = []

def configure_pins():
    global pins, adcs
    for i in range(0,22):
        p = Pin(i, Pin.IN, Pin.PULL_UP)
        pins.append((f"Pin{i:02d}",p))
    for i in range(26,28):
        adc = ADC(Pin(i))
        adcs.append((f"Adc{i:02d}", adc))

def show_pins():
    global pins, adcs    
    while True:
        for name, pin in pins:
            print(f"{name}:{pin.value()}  ", end="")
        for name, adc in adcs:
            print(f"{name}:{adc.read_u16()}  ", end="")
        print("")    
        sleep(0.05)

#i2c = I2C(0, scl=Pin(24), sda=Pin(25))
#display = adafruit_ht16k33.segments.Seg7x4(i2c)
#display.print(1234)

print("HERE")
configure_pins()
print("HERE2")
show_pins()

#blink()

