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

pixels = neopixel.NeoPixel(board.A1, 2, brightness=0.5)
pixels[0] = (255,255,0)

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
        
def breathe(pixelIndex):
    print("start breathe")
    currentBlue = curColor[pixelIndex]
    pixels[pixelIndex] = blues[currentBlue]
    curColor[pixelIndex] = (currentBlue + 1) % len(blues)
    print("end breathe")
    


while True:
    
    #if buttonA.value:
    #    play_file(audiofiles[0])
    
    
    if cpx.touch_A1:
        print('Touched C4')
        cpx.start_tone(C4)
    elif cpx.touch_A2:
        print('Touched D')
        cpx.start_tone(D4)
        breathe(0)
    elif cpx.touch_A3:
        print('Touched E')
        cpx.start_tone(E4)
        breathe(1)
    elif cpx.touch_A4:
        print('Touched F')
        cpx.start_tone(F4)
    elif cpx.touch_A5:
        print('Touched G')
        cpx.start_tone(G4)
    elif cpx.touch_A6 and not cpx.touch_A7:
        print('Touched A')
        cpx.start_tone(A4)
    elif cpx.touch_A7 and not cpx.touch_A6:
        print('Touched B')
        cpx.start_tone(B4)
    elif cpx.touch_A6 and cpx.touch_A7:
        print('Touched C5')
        cpx.start_tone(C5)
    else:
        cpx.stop_tone()
        clearPixels()
    time.sleep(0.1)
