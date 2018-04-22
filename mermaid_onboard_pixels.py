import audiobusio
import board
import array
import math
import time
from digitalio import DigitalInOut, Direction, Pull
import audioio
import neopixel


pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness= 0.05) #determine beightness (Value can be between 0 and 1)
outboards = neopixel.NeoPixel(board.A2, 1, brightness=0.5)



blues = [(0,51,51), (0,102,102), (0,153,153), (0,204,204), (0,255,255), (51,255,255), (102,255,255), (153,255,255), (204,255,255)]
reds = [(153,0,0)]
curPixel = 0

while True:
    print("on pixel ", curPixel)
    bluesCount = 0
    outboards[0] = blues[0]
    while bluesCount < len(blues):
        pixels[curPixel] = blues[bluesCount]
        time.sleep(0.1)
        bluesCount += 1
        
    curPixel = (curPixel + 1) % len(pixels)