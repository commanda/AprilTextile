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

def stamp_caterpillar(around_index, size, primary, secondary):
    start = floor(around_index - (size/2))
    stop = floor(around_index + (size/2)) 
    k = 0
    for i in range(start, stop, 1):
        color = primary
        if (k < size/3 or k >= (2*(size/3))):
            color = secondary
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

hour = 0
minute = 0
second = 0

party_pixels_index = 0

party_mode = True

while True:

    if party_mode == True:
        party_pixels_index = (party_pixels_index + 1) % len(party_pixels)
        neopixel_write(pin, party_pixels[party_pixels_index])      
        #neopixel_write(pin, bytes([int(i * self.brightness) for i in party_pixels[party_pixels_index]]))
        sleep(0.1)

    else:
        t = rtc.datetime

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
        