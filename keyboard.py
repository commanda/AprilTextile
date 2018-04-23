import time
from adafruit_circuitplayground.express import cpx

# Time needed to debounce button, in seconds
debounceTime = 0.2

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

while True:
    if cpx.touch_A1:
        print('Touched C')
        cpx.start_tone(C4)
    elif cpx.touch_A2:
        print('Touched D')
        cpx.start_tone(D4)
    elif cpx.touch_A3:
        print('Touched E')
        cpx.start_tone(E4)
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
    time.sleep(0.01)
