import time
import board
import curses
from adafruit_motorkit import MotorKit

from sensor import Sensor

class Drive(Sensor):
    def __init__(self, stop_event):
        self.kit = MotorKit(i2c=board.I2C())
        self.stop_event = stop_event

        self.M1SPEED = 1.0
        self.M2SPEED = -self.M1SPEED
        
    def start(self):
        curses.wrapper(self.get_key)

    def get_key(self, stdscr):
        curses.cbreak()
        stdscr.nodelay(True)
        stdscr.keypad(True)

        while not self.stop_event_is_set():
            key = stdscr.getch()
            if key == ord('w'):
                self.kit.motor1.throttle = self.M1SPEED
                self.kit.motor2.throttle = self.M2SPEED
            elif key == ord('s'):
                self.kit.motor1.throttle = -self.M1SPEED
                self.kit.motor2.throttle = -self.M2SPEED
            elif key == ord('a'):
                self.kit.motor1.throttle = -self.M1SPEED
                self.kit.motor2.throttle = self.M2SPEED
            elif key == ord('d'):
                self.kit.motor1.throttle = self.M1SPEED
                self.kit.motor2.throttle = -self.M2SPEED
            elif key == ord('q'):
                self.kit.motor1.throttle = 0
                self.kit.motor2.throttle = 0
                break
            else:
                self.kit.motor1.throttle = 0
                self.kit.motor2.throttle = 0

            time.sleep(0.025)

if __name__ == "__main__":
    import threading
    stop_event = threading.Event()
    d = Drive(stop_event)
    d.start()

