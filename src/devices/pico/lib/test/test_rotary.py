from machine import Pin
import time

# Rotary Encoder Pins
clk = Pin(17, Pin.IN, Pin.PULL_UP)  # A (CLK)
dt = Pin(18, Pin.IN, Pin.PULL_UP)   # B (DT)

counter = 0
last_clk_state = clk.value()

def rotary_changed(pin):
    global counter, last_clk_state
    
    clk_state = clk.value()
    dt_state = dt.value()

    print(f'CLK: {clk_state} DT: {dt_state}')

    if clk_state != last_clk_state:  # Change detected
        if dt_state != clk_state:
            print(f' Clockwise')
            counter += 1  # Clockwise
        else:
            counter -= 1  # Counterclockwise
            print(f' Counterclockwise')
        print(f"Counter: {counter}")  # Print new value
    
    last_clk_state = clk_state  # Update previous state

# Attach Interrupts to A (CLK) Pin
clk.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=rotary_changed)

while True:
    time.sleep(0.1)  # Prevent CPU overload
