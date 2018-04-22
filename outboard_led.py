import time
import board
import neopixel

pixel = neopixel.NeoPixel(board.A2, 1, brightness=0.5)
pixel[0] = (255,255,0)