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
t = rtc.datetime
hour = 0
minute = 0
second = 0
party_mode = True
party_len = 6

party_pixels = bytes([24,60,0, 26,63,0, 28,63,0, 30,63,0, 32,63,0, 34,63,0, 38,63,0, 39,63,0, 39,63,0, 38,63,3, 37,63,8, 35,62,13, 35,61,16, 35,61,16, 35,61,17, 38,63,19, 21,46,10, 1,17,0, 5,22,1, 7,30,1, 1,10,0, 1,9,0, 0,8,0, 0,5,0, 0,5,0, 0,4,0, 23,44,6, 32,59,7, 1,9,0, 1,10,0, 1,12,0, 0,5,0, 12,26,8, 42,57,34, 40,56,31, 39,57,29, 38,58,21, 40,63,20, 42,61,31, 42,57,33, 41,56,33, 41,55,34, 42,55,35, 42,55,35, 42,57,34, 42,59,33, 41,60,32, 40,60,31, 39,58,31, 36,56,30, 34,56,29, 34,58,28, 34,58,28, 32,57,26, 31,57,25, 34,57,29, 37,55,32, 38,51,34, 40,49,35, 43,49,37, 43,48,37, 44,46,38, 45,44,41, 44,45,41, 44,49,39, 43,54,36, 42,56,33, 42,58,31, 39,60,28, 36,61,22, 29,60,17, 19,54,13, 10,47,9, 5,45,7, 3,42,7, 5,41,9, 8,42,11, 12,44,15, 15,46,17, 18,47,19, 21,49,21, 23,49,23, 25,48,24, 24,45,25, 24,43,24, 24,42,25, 22,40,23, 22,38,23, 21,37,23, 19,36,22, 19,35,22, 16,33,20, 15,32,20, 18,34,22, 17,33,21, 14,32,20, 12,32,18, 11,32,18, 12,33,19, 10,31,18, 7,28,15, 5,25,14, 3,22,13, 2,20,12, 1,18,12, 1,17,11, 1,16,10, 1,15,10, 1,14,10, 1,13,9, 1,13,9, 1,13,9, 1,12,9, 1,13,9, 1,13,9, 1,14,9])

while True:
    t = rtc.datetime
    if party_mode == True:
        neopixel_write(pin, party_pixels)
        sleep(0.1)
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
        stamp_caterpillar(hour, 9, (150, 23, 19), (249, 153, 17))
        stamp_caterpillar(minute, 6, (2, 22, 242), (82, 143, 242))
        stamp_caterpillar(second, 3, (255,255,255), (255, 255, 0))
        neopixel_write(pin, buf)
        if t.tm_sec in range(0,party_len):
            party_mode = True
            clear()
        