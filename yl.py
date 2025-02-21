
import RPi.GPIO as GPIO
import time

MOISTURE_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(MOISTURE_PIN, GPIO.IN)

try:
    while True:
        moisture = GPIO.input(MOISTURE_PIN)
        print("Dry" if moisture else "Wet")
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()

