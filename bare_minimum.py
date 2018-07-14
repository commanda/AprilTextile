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
        buf[(i * bpp) + R] = black[R]
        buf[(i * bpp) + G] = black[G]
        buf[(i * bpp) + B] = black[B]
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
party_pixels_index = 0
party_mode = True
party_len = 6

party_pixels = bytes([241,98,1, 252,104,1, 255,112,1, 255,121,1, 254,131,1, 254,138,1, 254,153,1, 255,159,2, 255,156,0, 254,153,13, 253,149,32, 249,142,54, 246,142,67, 245,142,66, 244,140,69, 254,153,77, 186,85,40, 70,7,0, 91,20,5, 123,29,7, 41,5,2, 36,4,1, 35,3,2, 22,2,1, 21,3,1, 16,0,0, 176,92,24, 239,129,30, 38,4,2, 41,4,2, 48,7,3, 22,0,0, 104,48,34, 231,171,138, 225,162,125, 228,156,117, 235,153,86, 252,161,81, 246,171,127, 231,169,134, 225,167,134, 221,167,137, 222,170,141, 222,168,140, 230,169,137, 237,169,133, 242,167,129, 241,163,126, 234,156,125, 227,146,121, 226,139,116, 232,137,113, 234,138,112, 231,130,105, 229,126,102, 230,139,116, 221,149,130, 207,155,138, 197,161,141, 196,173,148, 192,174,149, 185,176,155, 177,180,167, 180,179,166, 197,177,157, 217,175,145, 224,170,133, 232,168,126, 240,159,112, 246,146,89, 243,117,69, 217,76,54, 190,40,38, 180,21,29, 169,14,30, 166,22,36, 170,32,46, 177,49,61, 184,61,70, 191,72,76, 196,84,85, 199,95,92, 194,102,99, 180,98,100, 172,97,99, 170,99,100, 160,90,93, 155,91,95, 151,86,93, 147,79,91, 143,76,90, 134,66,83, 130,61,80, 137,72,89, 135,69,87, 131,59,80, 128,49,74, 129,47,74, 133,51,79, 125,43,72, 113,29,62, 100,20,56, 91,14,53, 83,9,50, 75,6,48, 68,5,46, 65,4,43, 62,5,42, 59,5,41, 54,6,39, 53,6,39, 52,7,39, 50,7,38, 52,7,38, 53,6,37, 58,6,39, 62,5,41, 68,4,43, 71,4,45, 72,3,44])

while True:
    t = rtc.datetime
    if party_mode == True:
        for i in range(num_leds):
            buf[(i * bpp) + R] = randint(0,50)
            buf[(i * bpp) + G] = randint(0,50)
            buf[(i * bpp) + B] = randint(0,50)

        neopixel_write(pin, buf)
        #sleep(0.1)
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
        