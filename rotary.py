#!/usr/bin/env python3
"""
This Raspberry Pi code was developed by newbiely.com
This Raspberry Pi code is made available for public use without any restriction
For comprehensive instructions and wiring diagrams, please visit:
https://newbiely.com/tutorials/raspberry-pi/raspberry-pi-rotary-encoder
"""


import RPi.GPIO as GPIO
import time

from sensor import Sensor

# Pin numbers on Raspberry Pi
CLK_PIN = 13   # GPIO7 connected to the rotary encoder's CLK pin
DT_PIN = 18    # GPIO8 connected to the rotary encoder's DT pin

DIRECTION_CW = 0
DIRECTION_CCW = 1

direction = DIRECTION_CW

class Rotary(Sensor):
    def __init__(self):
        self.counter = 0
        self.CLK_state = 0
        self.CLK_PIN = 13
        self.DT_PIN = 18

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.CLK_PIN, GPIO.IN)
        GPIO.setup(self.DT_PIN, GPIO.IN)
        self.prev_CLK_state = GPIO.input(self.CLK_PIN)

    def start(self):
        try:
            while True:
                self.CLK_state = GPIO.input(self.CLK_PIN)

                if self.CLK_state != self.prev_CLK_state and self.CLK_state == GPIO.HIGH:
                    if GPIO.input(self.DT_PIN) == GPIO.HIGH:
                        self.counter -= 1
                        direction = DIRECTION_CCW
                    else:
                        self.counter += 1
                        direction = DIRECTION_CW
                    print(self.counter)
                self.prev_CLK_state = self.CLK_state
        except KeyboardInterrupt:
            GPIO.cleanup()


if __name__ == "__main__":
    r = Rotary()
    r.start()

