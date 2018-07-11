import board
import neopixel
from time import sleep, struct_time
import adafruit_ds3231
import busio
from math import floor

num_leds = 120

def stamp_caterpillar(around_index, size, primary, secondary):
    start = floor(around_index - (size/2))
    stop = floor(around_index + (size/2)) 
    k = 0
    for i in range(start, stop, 1):
        color = primary
        if (k < size/3 or k > (2*(size/3))):
            color = secondary
        outboards[i % num_leds]    = color
        k = k+1

def normalize(x, old_min, old_max, new_min, new_max):
    return (((x - old_min) / (old_max - old_min)) * (new_max - new_min)) + new_min

def put_value_into_pixels_range(x, max, num_leds):
    return floor(normalize(x, 0, max, 0, num_leds-1)) - 1

outboards = neopixel.NeoPixel(board.A1, num_leds, brightness=0.05, auto_write=False)


for i in range(num_leds):
    outboards[i] = (0,0,0)
    
    
outboards.show()

myI2C = busio.I2C(board.SCL, board.SDA)

rtc = adafruit_ds3231.DS3231(myI2C)

hour = 0
minute = 0
second = 0

black = (0,0,0)

while True:
    t = rtc.datetime

    stamp_caterpillar(hour, 10, black, black)
    stamp_caterpillar(minute, 6, black, black)
    stamp_caterpillar(second, 3, black, black)

    hour = put_value_into_pixels_range(t.tm_hour, 24, num_leds)
    minute = put_value_into_pixels_range(t.tm_min, 60, num_leds)
    second = put_value_into_pixels_range(t.tm_sec, 60, num_leds)
    
    stamp_caterpillar(hour, 10, (249, 124, 22), (247, 199, 27))
    stamp_caterpillar(minute, 6, (0,0,255), (82, 143, 242))
    stamp_caterpillar(second, 3, (0,255,0), (9, 2, 132))
    
    outboards.show()
    
    sleep(1)