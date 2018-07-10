import board
import neopixel
import time
#import adafruit_ds3231
import busio

outboards = neopixel.NeoPixel(board.A1, 120, brightness=0.05, auto_write=False)
color = (255,255,30)


# initialize the I2C bus
myI2C = busio.I2C(board.SCL, board.SDA)

while True:
    print("voila!")
    for i in range(len(outboards)):
        outboards[i] = color
    outboards.show()
    time.sleep(1)