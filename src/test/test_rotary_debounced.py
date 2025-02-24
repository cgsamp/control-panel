import micropython
import time
from machine import Pin
from rotary.rotary_irq_rp2 import RotaryIRQ


r0 = RotaryIRQ(pin_num_clk=14,
              pin_num_dt=9,
              min_val=0,
              max_val=49,
              pull_up=True,
              reverse=False,
              range_mode=RotaryIRQ.RANGE_BOUNDED)

r1 = RotaryIRQ(pin_num_clk=6,
              pin_num_dt=7,
              min_val=0,
              max_val=49,
              pull_up=True,
              reverse=False,
              range_mode=RotaryIRQ.RANGE_BOUNDED)

r2 = RotaryIRQ(pin_num_clk=0,
              pin_num_dt=1,
              min_val=0,
              max_val=49,
              pull_up=True,
              reverse=False,
              range_mode=RotaryIRQ.RANGE_BOUNDED)

print('Created rotary.')

val_old0 = r0.value()
val_old1 = r1.value()
val_old2 = r2.value()
while True:
    val_new0 = r0.value()
    val_new1 = r1.value()
    val_new2 = r2.value()
    print('.', end = '')

    if val_old0 != val_new0:
        val_old0 = val_new0
        print('result0 =', val_new0)

    if val_old1 != val_new1:
        val_old1 = val_new1
        print('result1 =', val_new1)

    if val_old2 != val_new2:
        val_old2 = val_new2
        print('result =', val_new2)

    time.sleep_ms(250)