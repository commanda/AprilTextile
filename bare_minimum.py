import board
import neopixel
from time import sleep
import adafruit_ds3231
import busio

num_leds = 120

def normalize(x, old_min, old_max, new_min, new_max):
    return (((x - old_min) / (old_max - old_min)) * (new_max - new_min)) + new_min

def put_value_into_pixels_range(x, max, num_leds):
    return num_leds - floor(normalize(x, 0, max, 0, num_leds-1)) - 1

outboards = neopixel.NeoPixel(board.A1, num_leds, brightness=0.05, auto_write=False)


for i in range(num_leds):
    outboards[i] = (255,255,0)
    
    
outboards.show()

# initialize the I2C bus
myI2C = busio.I2C(board.SCL, board.SDA)

# create the rtc object to talk to the rtc board
rtc = adafruit_ds3231.DS3231(myI2C)

while True:
    t = rtc.datetime
    
    print(t.tm_hour, t.tm_min, t.tm_sec)
    
    sleep(1)