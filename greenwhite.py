import digitalio
from neopixel_write import neopixel_write
import board
from math import floor

n = 120
bpp = 3
pin = digitalio.DigitalInOut(board.A1)
pin.direction = digitalio.Direction.OUTPUT
buf = bytearray(n * bpp)
brightness = 0.05
i = 0
mode = 0

green = (0,12,0)
white = (12,12,12)


while True:
    mode = (mode + 1) % 2
    for p in range(n):
        i = (i + 1) % n
        if mode == 0:
            buf[(i * bpp) + 0] = green[1]
            buf[(i * bpp) + 1] = green[0]
            buf[(i * bpp) + 2] = green[2]
        else:
            buf[(i * bpp) + 0] = white[1]
            buf[(i * bpp) + 1] = white[0]
            buf[(i * bpp) + 2] = white[2]
        neopixel_write(pin, buf)
    