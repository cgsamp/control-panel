from machine import Pin, I2C
from hybotics_ht16k33.segments import Seg7x4

SCL = Pin(21,Pin.IN,Pin.PULL_UP)
SDA = Pin(20,Pin.IN,Pin.PULL_UP)

i2c = I2C(0,sda=SDA,scl=SCL, freq=400000)

devices = i2c.scan()
segment_display_address = devices.pop()

display = Seg7x4(i2c)
display.print('0010')
display.blink_rate = 0
display.colon = True

# blink_rate
# brightness
# auto_write
# show
# scroll
# colon




#print(f'scans={i2c.scan()}')

#i2c.writeto(42, b'123')         # write 3 bytes to peripheral with 7-bit address 42
#i2c.readfrom(42, 4)             # read 4 bytes from peripheral with 7-bit address 42

#i2c.readfrom_mem(42, 8, 3)      # read 3 bytes from memory of peripheral 42,
                                #   starting at memory-address 8 in the peripheral
#i2c.writeto_mem(42, 2, b'\x10') # write 1 byte to memory of peripheral 42
 
 
    