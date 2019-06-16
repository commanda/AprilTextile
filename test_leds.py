import board
import digitalio
from neopixel_write import neopixel_write
G = 0
R = 1
B = 2
num_leds = 120
bpp = 3
buf = bytearray(num_leds * bpp)

pin = digitalio.DigitalInOut(board.A1)
pin.direction = digitalio.Direction.OUTPUT

black = (255,255,0)
for i in range(num_leds):
    buf[(i * bpp) + 0] = black[R]
    buf[(i * bpp) + 1] = black[G]
    buf[(i * bpp) + 2] = black[B]

neopixel_write(pin, buf)