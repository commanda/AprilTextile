import board
from neopixel_write import neopixel_write
from time import sleep
import busio
import digitalio
from rainbow_circle import party_pixels

G = 0
R = 1
B = 2
num_leds = 120
bpp = 3
buf = bytearray(num_leds * bpp)
pin = digitalio.DigitalInOut(board.A1)
pin.direction = digitalio.Direction.OUTPUT

pp_len = len(party_pixels)
p = 0

black = (0,0,0)

while True:
    for i in range(num_leds):
        buf[(i * bpp) + R] = party_pixels[(((i + p) * bpp) % pp_len) + R]
        buf[(i * bpp) + G] = party_pixels[(((i + p) * bpp) % pp_len) + G]
        buf[(i * bpp) + B] = party_pixels[(((i + p) * bpp) % pp_len) + B]
    
    neopixel_write(pin, buf)
    p = (p + 1) % num_leds
