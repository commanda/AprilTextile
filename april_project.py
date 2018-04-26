import time
from adafruit_circuitplayground.express import cpx
import board
import neopixel
from digitalio import DigitalInOut, Direction, Pull
import audioio
from random import randint

def smart_delay(delay: float, last_time: float) -> float:
    """
    A "smart" delay mechanism which tries to reduce the
    delay as much as possible based on the time the last
    delay happened.

    :param delay: delay in seconds
    :param last_cmd: time of last command
    :param remain: counter, skip delay unless it's zero

    :return: timestamp to feed to next invocation
    """
    now = time.monotonic()
    if delay > 0.0:

        delta = now - last_time
        if delta < delay:
            sleep = delay - delta
            time.sleep(sleep)

    return time.monotonic() 

#def setColor():

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

    tick_time = time.monotonic()
    count = 0
    while True:
        count += 1
        for i in range(len(outboardPixels)):
            outboardPixels[i] = (randint(0,255),randint(0,255),randint(0,255))
        pixels.show()
        tick_time = smart_delay(0.1, tick_time)
    
    
    

main()
