import board
import digitalio
from neopixel_write import neopixel_write
from time import sleep, struct_time
import adafruit_ds3231
import busio
from math import floor
from whole_image_party_pixels import party_pixels

G = 0
R = 1
B = 2

num_leds = 120
bpp = 3
buf = bytearray(num_leds * bpp)

pin = digitalio.DigitalInOut(board.A1)
pin.direction = digitalio.Direction.OUTPUT

dim_ratio = 0.05

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
for i in range(num_leds):
    buf[(i * bpp) + R] = black[R]
    buf[(i * bpp) + G] = black[G]
    buf[(i * bpp) + B] = black[B]
neopixel_write(pin, buf)  

myI2C = busio.I2C(board.SCL, board.SDA)

rtc = adafruit_ds3231.DS3231(myI2C)

t = rtc.datetime

hour = 0
minute = 0
second = 0

party_pixels_index = 0

party_mode = False

while True:
    t = rtc.datetime
    if party_mode == True:
        party_pixels_index = (party_pixels_index + 1) % len(party_pixels)
        row = party_pixels[party_pixels_index]
        for i in range(len(row)):
            buf[(i * bpp) + R] = row[i]

        neopixel_write(pin, buf)
        sleep(0.1)
        if t.tm_sec not in range(0,10):
            party_mode = False

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

        if t.tm_sec in range(0,10):
            party_mode = True
        