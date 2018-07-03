import time
from adafruit_circuitplayground.express import cpx
import board
import neopixel
from digitalio import DigitalInOut, Direction, Pull
import audioio
from random import randint


# constants
led_pin = board.A1
num_outboard_leds = 120
num_onboard_leds = 10
outboard_brightness = 0.5
onboard_brightness = 0.05
RED = 0
GREEN = 1
BLUE = 2


onboardPixels = neopixel.NeoPixel(board.NEOPIXEL, num_onboard_leds, brightness=onboard_brightness, auto_write=False)

outboardPixels = neopixel.NeoPixel(led_pin, num_outboard_leds, brightness=outboard_brightness, auto_write=False)

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

button_state = False
def clearPixels(pixels):
    set_pixels_color(pixels, (0,0,0))

def handle_button():
    global button_state
    if (button_state != cpx.button_a):
        button_state = cpx.button_a

        if button_state:
            cpx.red_led = True
            set_pixels_color(onboardPixels, (255,255,255))
        else:
            cpx.red_led = False
            clearPixels(onboardPixels)

def main():

    print("start")

    clearPixels(onboardPixels)
    clearPixels(outboardPixels)

    # spkrenable = DigitalInOut(board.SPEAKER_ENABLE)

    while True:
        handle_button()


main()
