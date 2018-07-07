import adafruit_ds3231
import time
import busio
import neopixel
import board
from math import *

# constants
led_pin = board.A1
num_outboard_leds = 85
num_onboard_leds = 10
outboard_brightness = 0.5
onboard_brightness = 0.05
RED = 0
GREEN = 1
BLUE = 2
minute_color = (44, 159, 247)
hour_color = (244, 191, 66)
second_color = (249, 246, 57)

# initialize the I2C bus
myI2C = busio.I2C(board.SCL, board.SDA)
# create the rtc object to talk to the rtc board
rtc = adafruit_ds3231.DS3231(myI2C)

# initialize the time - set this to the current time if we need to reset the clock
#rtc.datetime = time.struct_time((2018,7,6,22,33,0,0,9,-1))

onboard_pixels = neopixel.NeoPixel(board.NEOPIXEL, num_onboard_leds, brightness=onboard_brightness, auto_write=False)
#outboard_pixels = neopixel.NeoPixel(led_pin, num_outboard_leds, brightness=outboard_brightness, auto_write=False)

#pixels = outboard_pixels
#num_leds = num_outboard_leds
pixels = onboard_pixels
num_leds = num_onboard_leds


def smart_delay(delay: float, last_time: float) -> float:
    now = time.monotonic()
    if delay > 0.0:

        delta = now - last_time
        if delta < delay:
            sleep = delay - delta
            time.sleep(sleep)

    return time.monotonic()

def set_pixels_color(pixels, color):
    for i in range(len(pixels)):
        pixels[i] = color

def clear_pixels(pixels):
    set_pixels_color(pixels, (0,0,0))

def normalize(x, old_min, old_max, new_min, new_max):
    return (((x - old_min) / (old_max - old_min)) * (new_max - new_min)) + new_min

def put_value_into_pixels_range(x, max, num_leds):
    return num_leds - floor(normalize(x, 0, max, 0, num_leds-1)) - 1

while True:
    start_time = time.monotonic()
    t = rtc.datetime

    # animate the pixels
    hour = put_value_into_pixels_range(t.tm_hour, 24, num_leds)
    minute = put_value_into_pixels_range(t.tm_min, 60, num_leds)
    second = put_value_into_pixels_range(t.tm_sec, 60, num_leds)


    print(t.tm_hour, t.tm_min, t.tm_sec)
    print(hour, minute, second)

    clear_pixels(pixels)
    pixels[hour] = hour_color
    pixels[minute] = minute_color
    pixels[second] = second_color
    pixels.show()

    tick_time = start_time
    tick_time = smart_delay(1.0, tick_time)
