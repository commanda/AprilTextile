import time
from adafruit_circuitplayground.express import cpx
import board
import neopixel
from digitalio import DigitalInOut, Direction, Pull
import audioio

print("start")

# set up note values in Hz. Find frequency values at https://pages.mtu.edu/~suits/notefreqs.html
Ab3 = 208
A3 = 223
As3 = 233
Bb3 = 233
B3 = 247
C4 = 262
Cs4 = 277
Db4 = 277
D4 = 294
Ds4 = 311
Eb4 = 311
E4 = 330
F4 = 349
Fs4 = 370
Gb4 = 370
G4 = 392
Gs4 = 415
A4 = 440
B4 = 494
C5 = 523

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.05, auto_write=False)
pixels[0] = (255,255,0)

curColor = []
for i in range(len(pixels)):
    curColor.append(0)

bluesStart = [(0,51,51), (0,102,102), (0,153,153), (0,204,204), (0,255,255), (51,255,255), (102,255,255), (153,255,255), (204,255,255)]
# sentry-march the blues
bluesCopy = bluesStart.copy()
bluesStart.reverse()
blues = bluesCopy + bluesStart


def set_pixels_color(pixels, color):
    for i in range(len(pixels)):
        pixels[i] = color
    pixels.show()

def clearPixels(pixels):
    set_pixels_color(pixels, (0,0,0))
        

while True:
    
    if cpx.touch_A1:
        print('Touched C')
        cpx.start_tone(C4)
        set_pixels_color(pixels, (255,0,0))
    elif cpx.touch_A2:
        print('Touched D')
        cpx.start_tone(D4)
        set_pixels_color(pixels, (255, 153, 0))
    elif cpx.touch_A3:
        print('Touched E')
        cpx.start_tone(E4)
        set_pixels_color(pixels, (255, 255, 0))
    elif cpx.touch_A4:
        print('Touched F')
        cpx.start_tone(F4)
        set_pixels_color(pixels, (51, 204, 51))
    elif cpx.touch_A5:
        print('Touched G')
        cpx.start_tone(G4)
        set_pixels_color(pixels, (51, 153, 255))
    elif cpx.touch_A6 and not cpx.touch_A7:
        print('Touched A')
        cpx.start_tone(A4)
        set_pixels_color(pixels, (0, 0, 153))
    elif cpx.touch_A7 and not cpx.touch_A6:
        print('Touched B')
        cpx.start_tone(B4)
        set_pixels_color(pixels, (153, 51, 255))
    elif cpx.touch_A6 and cpx.touch_A7:
        print('Touched C5')
        cpx.start_tone(C5)
        set_pixels_color(pixels, (204, 0, 204))
    else:
        cpx.stop_tone()
        clearPixels(pixels)
    time.sleep(0.1)
