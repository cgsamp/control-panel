from machine import Pin, I2C

i2c = I2C(0, scl=Pin(5), sda=Pin(4))
addr_list = i2c.scan()
addr = addr_list.pop()
print(f'Address: {addr}')

# Enable the display
i2c.writeto(addr, bytearray([0x21]))  # Turn on oscillator
i2c.writeto(addr, bytearray([0x81]))  # Turn on display, no blinking
i2c.writeto(addr, bytearray([0xE0 | 15]))  # Set brightness to max

# Segment mappings for digits 0-9
digit_map = {
    0: 0x3F, 
    1: 0x06, 
    2: 0x5B, 
    3: 0x4F,
    4: 0x66, 
    5: 0x6D, 
    6: 0x7D, 
    7: 0x07,
    8: 0x7F, 
    9: 0x6F
}

for digit in digit_map:
    print(f'Digit: {digit:08b} {digit:02x} {digit:02d}')

# Number to display (e.g., "1234")
num = [1, 2, 3, 4]

data = bytearray([
    0x00, digit_map[num[0]],  # Digit 1 (Rightmost)
    0x02, digit_map[num[1]],  # Digit 2
    0x04, 0x02,  # **Colon ON (was misaligned before)**
    0x06, digit_map[num[2]],  # Digit 3
    0x08, digit_map[num[3]],  # Digit 4 (Leftmost)
    0x0A, 0x00,  # Unused segments
    0x0C, 0x00,
    0x0E, 0x00
])

# Send data to HT16K33
i2c.writeto(addr, data)

print("Displayed: 1234")
