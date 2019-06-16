import board
from neopixel_write import neopixel_write
from time import sleep
import busio
import digitalio

G = 0
R = 1
B = 2
num_leds = 120
bpp = 3
buf = bytearray(num_leds * bpp)
pin = digitalio.DigitalInOut(board.A1)
pin.direction = digitalio.Direction.OUTPUT

# satin waterfall blue colors
party_pixels = bytes([5,1,11, 4,1,11, 3,0,10, 2,0,9, 3,0,10, 3,1,10, 1,0,9, 2,0,9, 2,0,10, 3,0,10, 4,1,11, 4,1,11, 5,1,11, 5,1,11, 5,1,11, 5,1,11, 6,1,11, 6,2,11, 6,2,11, 6,2,11, 6,2,11, 7,2,12, 6,2,11, 7,2,12, 6,1,11, 6,1,11, 7,2,12, 7,2,12, 7,2,12, 7,2,12, 6,2,12, 3,0,11, 0,0,6, 0,0,4, 0,0,5, 1,0,6, 1,0,6, 1,0,7, 1,0,7, 1,0,7, 1,0,7, 1,0,7, 1,0,7, 1,0,7, 1,0,7, 1,0,8, 1,0,8, 2,0,10, 3,0,11, 2,0,8, 0,0,3, 0,0,4, 1,0,7, 2,0,9, 4,1,10, 5,1,11, 6,2,12, 6,2,12, 5,1,11, 4,1,11, 4,1,11, 6,1,12, 3,1,7, 0,0,3, 1,0,8, 3,0,10, 6,2,12, 2,0,10, 1,0,7, 1,0,8, 1,0,9, 4,1,10, 4,1,10, 0,0,5, 0,0,2, 0,0,4, 0,0,5, 0,0,6, 0,0,5, 0,0,5, 1,0,8, 1,0,9, 2,0,9, 2,0,10, 3,1,10, 6,2,11, 5,2,11, 3,0,10, 2,0,9, 1,0,7, 1,0,6, 0,0,4, 1,0,7, 4,1,11, 6,2,11, 6,2,11, 5,1,11, 4,0,11, 2,0,10, 2,0,9, 2,0,9, 2,0,9, 1,0,9, 1,0,8, 1,0,7, 1,0,6, 0,0,6, 0,0,5, 4,1,10, 6,1,11, 5,1,11, 5,1,11, 4,1,10, 4,1,11, 6,2,12, 5,1,11, 4,1,10, 3,0,10, 2,0,10, 2,0,9])

pp_len = len(party_pixels)
p = 0

black = (0,0,0)

while True:
    for i in range(num_leds):
        if i < num_leds/2:
            pix = i * bpp
        else:
            pix = (num_leds - 1 - (i - int(num_leds/2))) * bpp
    
        buf[pix + R] = party_pixels[(((i + p) * bpp) % pp_len) + R]
        buf[pix + G] = party_pixels[(((i + p) * bpp) % pp_len) + G]
        buf[pix + B] = party_pixels[(((i + p) * bpp) % pp_len) + B]
    neopixel_write(pin, buf)
    p = (p - 1) % int(pp_len/bpp)
