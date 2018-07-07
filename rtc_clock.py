import adafruit_ds3231
import time
import busio
from board import *

myI2C = busio.I2C(SCL, SDA)
rtc = adafruit_ds3231.DS3231(myI2C)

# initialize the time - set this to the current time if we need to reset the clock
#rtc.datetime = time.struct_time((2018,7,6,22,33,0,0,9,-1))

def smart_delay(delay: float, last_time: float) -> float:
    now = time.monotonic()
    if delay > 0.0:

        delta = now - last_time
        if delta < delay:
            sleep = delay - delta
            time.sleep(sleep)

    return time.monotonic()


while True:
    start_time = time.monotonic()
    t = rtc.datetime
    print(t.tm_hour, t.tm_min, t.tm_sec)
    tick_time = start_time
    tick_time = smart_delay(1.0, tick_time)
