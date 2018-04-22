import board
import digitalio
import time

led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

while True:
    print("voila!")
    led.value = True
    time.sleep(1)
    led.value = False
    time.sleep(1)