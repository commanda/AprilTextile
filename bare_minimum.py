import board
import digitalio
from neopixel_write import neopixel_write
from time import sleep, struct_time
import adafruit_ds3231
import busio
from math import floor
from random import randint

G = 0
R = 1
B = 2
num_leds = 120
bpp = 3
buf = bytearray(num_leds * bpp)
pin = digitalio.DigitalInOut(board.A1)
pin.direction = digitalio.Direction.OUTPUT
dim_ratio = 0.05

def clear():
    for i in range(num_leds):
        buf[(i * bpp) + 0] = black[R]
        buf[(i * bpp) + 1] = black[G]
        buf[(i * bpp) + 2] = black[B]
    neopixel_write(pin, buf)  

def stamp_caterpillar(around_index, size, primary, secondary):
    start = floor(around_index - (size/2))
    stop = floor(around_index + (size/2)) 

    # the center pixel should be bright, and all other pixels should be dimmer
    primary_dim = ((int)(primary[0] * dim_ratio), (int)(primary[1] * dim_ratio), (int)(primary[2] * dim_ratio))
    secondary_dim = ((int)(secondary[0] * dim_ratio), (int)(secondary[1] * dim_ratio), (int)(secondary[2] * 0.5))

    k = 0
    for i in range(start, stop, 1):
        color = primary_dim
        if (k < size/3 or k >= (2*(size/3))):
            color = secondary_dim
        elif (i == around_index):
            color = primary
        q = i % num_leds
        buf[(q * bpp) + 0] = color[R]
        buf[(q * bpp) + 1] = color[G]
        buf[(q * bpp) + 2] = color[B]
        
        k = k+1

def normalize(x, old_min, old_max, new_min, new_max):
    return (((x - old_min) / (old_max - old_min)) * (new_max - new_min)) + new_min

def put_value_into_pixels_range(x, max, num_leds):
    return floor(normalize(x, 0, max, 0, num_leds-1)) - 1

black = (0,0,0)
clear()
myI2C = busio.I2C(board.SCL, board.SDA)
rtc = adafruit_ds3231.DS3231(myI2C)
#rtc.datetime = struct_time((2018,7,17,7,15,10,0,9,-1))
t = rtc.datetime
hour = 0
minute = 0
second = 0
party_mode = True
party_len = 5

party_pixels = bytes([5,1,11, 4,1,11, 3,0,10, 2,0,9, 3,0,10, 3,1,10, 1,0,9, 2,0,9, 2,0,10, 3,0,10, 4,1,11, 4,1,11, 5,1,11, 5,1,11, 5,1,11, 5,1,11, 6,1,11, 6,2,11, 6,2,11, 6,2,11, 6,2,11, 7,2,12, 6,2,11, 7,2,12, 6,1,11, 6,1,11, 7,2,12, 7,2,12, 7,2,12, 7,2,12, 6,2,12, 3,0,11, 0,0,6, 0,0,4, 0,0,5, 1,0,6, 1,0,6, 1,0,7, 1,0,7, 1,0,7, 1,0,7, 1,0,7, 1,0,7, 1,0,7, 1,0,7, 1,0,8, 1,0,8, 2,0,10, 3,0,11, 2,0,8, 0,0,3, 0,0,4, 1,0,7, 2,0,9, 4,1,10, 5,1,11, 6,2,12, 6,2,12, 5,1,11, 4,1,11, 4,1,11, 6,1,12, 3,1,7, 0,0,3, 1,0,8, 3,0,10, 6,2,12, 2,0,10, 1,0,7, 1,0,8, 1,0,9, 4,1,10, 4,1,10, 0,0,5, 0,0,2, 0,0,4, 0,0,5, 0,0,6, 0,0,5, 0,0,5, 1,0,8, 1,0,9, 2,0,9, 2,0,10, 3,1,10, 6,2,11, 5,2,11, 3,0,10, 2,0,9, 1,0,7, 1,0,6, 0,0,4, 1,0,7, 4,1,11, 6,2,11, 6,2,11, 5,1,11, 4,0,11, 2,0,10, 2,0,9, 2,0,9, 2,0,9, 1,0,9, 1,0,8, 1,0,7, 1,0,6, 0,0,6, 0,0,5, 4,1,10, 6,1,11, 5,1,11, 5,1,11, 4,1,10, 4,1,11, 6,2,12, 5,1,11, 4,1,10, 3,0,10, 2,0,10, 2,0,9])

p = 0
party_pixels_len = len(party_pixels)

while True:
    t = rtc.datetime
    if party_mode == True:
        for i in range(num_leds):
            if i < num_leds/2:
                pix = i * bpp
            else:
                pix = (num_leds - 1 - (i - int(num_leds/2))) * bpp
        
            buf[pix + R] = party_pixels[(((i + p) * bpp) % party_pixels_len) + R]
            buf[pix + G] = party_pixels[(((i + p) * bpp) % party_pixels_len) + G]
            buf[pix + B] = party_pixels[(((i + p) * bpp) % party_pixels_len) + B]
        neopixel_write(pin, buf)
        p = (p - 1) % int(party_pixels_len/bpp)
        if t.tm_sec not in range(0,party_len):
            party_mode = False
            clear()

    else:
        stamp_caterpillar(hour, 10, black, black)
        stamp_caterpillar(minute, 6, black, black)
        stamp_caterpillar(second, 3, black, black)
        tmp_hour = t.tm_hour
        if (tmp_hour >= 12):
            tmp_hour = tmp_hour - 12
        hour = put_value_into_pixels_range(tmp_hour, 12, num_leds)
        minute = put_value_into_pixels_range(t.tm_min, 60, num_leds)
        second = put_value_into_pixels_range(t.tm_sec, 60, num_leds)
        stamp_caterpillar(hour, 9, (239, 119, 235), (145, 4, 140))
        stamp_caterpillar(minute, 6, (217, 146, 244), (110, 27, 142))
        stamp_caterpillar(second, 3, (242, 186, 237), (122, 68, 117))
        neopixel_write(pin, buf)
        if t.tm_sec in range(0,party_len):
            party_mode = True
            clear()
        