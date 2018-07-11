import board
import neopixel
from time import sleep
from math import floor

num_leds = 120

outboards = neopixel.NeoPixel(board.A1, num_leds, brightness=0.25, auto_write=False)

chosen_blue = 110
blue = (0,0,255)
light_blue = (82, 143, 242)

chosen_red = chosen_blue - 35
red = (249, 124, 22)
orange = (247, 199, 27)

chosen_white = chosen_red - 50
white = (0,255,0)
dark_blue = (9, 2, 132)

def stamp_caterpillar(around_index, size, primary, secondary):
    start = floor(around_index - (size/2))
    stop = floor(around_index + (size/2)) 
    k = 0
    for i in range(start, stop, 1):
        color = primary
        if (k < size/3 or k > (2*(size/3))):
            color = secondary
        outboards[i % num_leds]    = color
        k = k+1
    

while True:
    for i in range(num_leds):
        outboards[i] = (0,0,0)
    
    chosen_blue = (chosen_blue + 1) % num_leds
    chosen_red = (chosen_red - 1) % num_leds
    chosen_white = (chosen_white +1) % num_leds

    stamp_caterpillar(chosen_red, 20, orange, red)
    stamp_caterpillar(chosen_blue, 5, blue, light_blue)
    stamp_caterpillar(chosen_white, 10, white, dark_blue)
    
    outboards.show()
    sleep(0.01)