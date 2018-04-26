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

def clearPixels(pixels):
    for i in range(len(pixels)):
        pixels[i] = (0,0,0)
    pixels.show()

def main():

    print("start")

    onboardPixels = neopixel.NeoPixel(board.NEOPIXEL, 10, auto_write=False)

    outboardPixels = neopixel.NeoPixel(board.A1, 120, brightness=0.05, auto_write=False)

    pixels = outboardPixels

    clearPixels(pixels)

    
    start_time = time.monotonic()
    tick_time = start_time
    
    tween_time = 2.0
    
    while True:
        time_since_start = tick_time - start_time
        normalized_t = normalize(time_since_start % tween_time, 0, tween_time)
        color = color_tween((255,165,0), (0,0,255), normalized_t)
        print("normalized_t: ",normalized_t)
        for i in range(len(outboardPixels)):
            pixels[i] = color
            #outboardPixels[i] = (randint(0,255),randint(0,255),randint(0,255))
        pixels.show()
        tick_time = smart_delay(0.1, tick_time)
    

main()
