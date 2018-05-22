import time
from adafruit_circuitplayground.express import cpx
import board
import neopixel
from digitalio import DigitalInOut, Direction, Pull
import audioio
from random import randint

# constants 
RED = 0
GREEN = 1
BLUE = 2

def smart_delay(delay: float, last_time: float) -> float:
    now = time.monotonic()
    if delay > 0.0:

        delta = now - last_time
        if delta < delay:
            sleep = delay - delta
            time.sleep(sleep)

    return time.monotonic() 

def normalize(x, min, max):
    return (x - min) / (max - min)

def lerp(v0, v1, t):
    return (1.0 - t) * v0 + t * v1
    
def color_tween(color0, color1, t):
    return (int(lerp(color0[RED], color1[RED], t)), int(lerp(color0[GREEN], color1[GREEN], t)), int(lerp(color0[BLUE], color1[BLUE], t)))

def set_pixels_color(pixels, color):
    for i in range(len(pixels)):
        pixels[i] = color
    pixels.show()

def clearPixels(pixels):
    set_pixels_color(pixels, (0,0,0))
    
def bounds(v, l, h):
    if(v < l):
        v = l
    if(v > h):
        v = h
    return v
        

def main():

    print("start")

    onboardPixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.05, auto_write=False)

    outboardPixels = neopixel.NeoPixel(board.A1, 120, brightness=0.05, auto_write=False)


    clearPixels(onboardPixels)
    clearPixels(outboardPixels)

    
    start_time = time.monotonic()
    tick_time = start_time
    
    tween_time = 4.0
    

# not a great one, but it works, and it's tweakable.  You'll need to add imports and tweak values

    # strand = neopixel.NeoPixel(NEOPIXEL, 10, 3, 1, False)
    while True:
        r = 226
        g = 121
        b = 35

        #Flicker, based on our initial RGB values
        for i in range (0, len(outboardPixels)):
            flicker = randint(0,110)
            r1 = bounds(r-flicker, 0, 255)
            g1 = bounds(g-flicker, 0, 255)
            b1 = bounds(b-flicker, 0, 255)
            outboardPixels[i] = (r1,g1,b1)
        outboardPixels.show()
        time.sleep(randint(100,1000) / 3000)
    

main()
