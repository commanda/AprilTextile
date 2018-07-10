import board
import neopixel
from time import sleep
import adafruit_ds3231
import busio
from math import floor

num_leds = 120

def normalize(x, old_min, old_max, new_min, new_max):
    return (((x - old_min) / (old_max - old_min)) * (new_max - new_min)) + new_min

def put_value_into_pixels_range(x, max, num_leds):
    return num_leds - floor(normalize(x, 0, max, 0, num_leds-1)) - 1

outboards = neopixel.NeoPixel(board.A1, num_leds, brightness=0.05, auto_write=False)


for i in range(num_leds):
    outboards[i] = (0,0,0)
    
    
outboards.show()

# initialize the I2C bus
myI2C = busio.I2C(board.SCL, board.SDA)

# create the rtc object to talk to the rtc board
rtc = adafruit_ds3231.DS3231(myI2C)

# indexes into our pixels array to represent the clock hands
hour = 0
minute = 0
second = 0

while True:
    t = rtc.datetime
    
    #print(t.tm_hour, t.tm_min, t.tm_sec)
    outboards[hour] = (0,0,0)
    outboards[minute] = (0,0,0)
    outboards[second] = (0,0,0)
    #outboards.show()
    hour = put_value_into_pixels_range(t.tm_hour, 24, num_leds)
    minute = put_value_into_pixels_range(t.tm_min, 60, num_leds)
    second = put_value_into_pixels_range(t.tm_sec, 60, num_leds)
    
    outboards[hour] = (244, 191, 66)
    outboards[minute] = (44, 159, 247)
    outboards[second] = (249, 246, 57)
    outboards.show()
    print(hour)
    
    sleep(1)