from board import A1
import neopixel
import time

outboards = neopixel.NeoPixel(A1, 120, brightness=0.05, auto_write=False)
color = (255,255,30)
while True:
    print("voila!")
    for i in range(len(outboards)):
        outboards[i] = color
    outboards.show()
    time.sleep(1)