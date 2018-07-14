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

party_pixels = bytes([98,241,1, 104,252,1, 112,255,1, 121,255,1, 131,254,1, 138,254,1, 153,254,1, 159,255,2, 156,255,0, 153,254,13, 149,253,32, 142,249,54, 142,246,67, 142,245,66, 140,244,69, 153,254,77, 85,186,40, 7,70,0, 20,91,5, 29,123,7, 5,41,2, 4,36,1, 3,35,2, 2,22,1, 3,21,1, 0,16,0, 92,176,24, 129,239,30, 4,38,2, 4,41,2, 7,48,3, 0,22,0, 48,104,34, 171,231,138, 162,225,125, 156,228,117, 153,235,86, 161,252,81, 171,246,127, 169,231,134, 167,225,134, 167,221,137, 170,222,141, 168,222,140, 169,230,137, 169,237,133, 167,242,129, 163,241,126, 156,234,125, 146,227,121, 139,226,116, 137,232,113, 138,234,112, 130,231,105, 126,229,102, 139,230,116, 149,221,130, 155,207,138, 161,197,141, 173,196,148, 174,192,149, 176,185,155, 180,177,167, 179,180,166, 177,197,157, 175,217,145, 170,224,133, 168,232,126, 159,240,112, 146,246,89, 117,243,69, 76,217,54, 40,190,38, 21,180,29, 14,169,30, 22,166,36, 32,170,46, 49,177,61, 61,184,70, 72,191,76, 84,196,85, 95,199,92, 102,194,99, 98,180,100, 97,172,99, 99,170,100, 90,160,93, 91,155,95, 86,151,93, 79,147,91, 76,143,90, 66,134,83, 61,130,80, 72,137,89, 69,135,87, 59,131,80, 49,128,74, 47,129,74, 51,133,79, 43,125,72, 29,113,62, 20,100,56, 14,91,53, 9,83,50, 6,75,48, 5,68,46, 4,65,43, 5,62,42, 5,59,41, 6,54,39, 6,53,39, 7,52,39, 7,50,38, 7,52,38, 6,53,37, 6,58,39, 5,62,41])

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
        