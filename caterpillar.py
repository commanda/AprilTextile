import board
import neopixel
from time import sleep
from math import floor

num_leds = 120

outboards = neopixel.NeoPixel(board.A1, num_leds, brightness=0.05, auto_write=False)

chosen = 110
chosen_color = (0,0,255)
secondary_chosen_color = (82, 143, 242)

def stamp_caterpillar(around_index, size):
    start = floor(around_index - (size/2))
    stop = floor(around_index + (size/2)) 
    k = 0
    for i in range(start, stop, 1):
        color = chosen_color
        if (k < size/3 or k > (2*(size/3))):
            color = secondary_chosen_color
        outboards[i % num_leds]    = color
        k = k+1
    
    #outboards[(chosen-1) % num_leds]    = chosen_color
    #outboards[chosen]                   = chosen_color
    #outboards[(chosen+1) % num_leds]    = chosen_color
    
    #outboards[(chosen+2) % num_leds]    = secondary_chosen_color
    #outboards[(chosen+3) % num_leds]    = secondary_chosen_color

while True:
    for i in range(num_leds):
        outboards[i] = (255,255,0)
    
    chosen = (chosen + 1) % num_leds

    stamp_caterpillar(chosen, 12)
    
    outboards.show()
    sleep(0.01)