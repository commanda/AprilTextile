import time
from adafruit_circuitplayground.express import cpx
import board
import neopixel
from digitalio import DigitalInOut, Direction, Pull
import audioio

# enable the speaker
#speakerEnable = DigitalInOut(board.SPEAKER_ENABLE)
#speakerEnable.direction = Direction.OUTPUT
#speakerEnable.value = True

# make the 2 input buttons
#buttonA = DigitalInOut(board.BUTTON_A)
#buttonA.direction = Direction.INPUT
#button.pull = Pull.DOWN
#buttonB = DigitalInOut(board.BUTTON_B)
#buttonB.direction = Direction.INPUT
#buttonB.pull = Pull.DOWN

audiofiles = ["rimshot.wav"]

def play_file(filename):
    print("playing file " + filename)
    f = open(filename, "rb")
    a = audioio.AudioOut(board.SPEAKER, f)
    a.play()
    while a.playing:
        pass
    print("finished")
    
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


#onboardPixels = neopixel.NeoPixel(board.NEOPIXEL, 10, auto_write=False)

outboardPixels = neopixel.NeoPixel(board.A1, 120, brightness=0.05, auto_write=False)

pixels = outboardPixels

curColor = []
for i in range(len(pixels)):
    curColor.append(0)

bluesStart = [(0,51,51), (0,102,102), (0,153,153), (0,204,204), (0,255,255), (51,255,255), (102,255,255), (153,255,255), (204,255,255)]
# sentry-march the blues
bluesCopy = bluesStart.copy()
bluesStart.reverse()
blues = bluesCopy + bluesStart


def clearPixels():
    for i in range(len(pixels)):
        pixels[i] = (0,0,0)
    pixels.show()


clearPixels()
count = 0
while True:
    print("yo ",count)
    for i in range(len(outboardPixels)):
        outboardPixels[i] = blues[count]
    pixels.show()
    count = (count + 1) % len(blues)
    time.sleep(0.1)
    
