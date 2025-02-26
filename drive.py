import time
import board
import curses
from adafruit_motorkit import MotorKit

kit = MotorKit(i2c=board.I2C())

M1SPEED = 1.0
M2SPEED = -M1SPEED

def get_key(stdscr):
    curses.cbreak()
    stdscr.nodelay(True)
    stdscr.keypad(True)

    while True:
        key = stdscr.getch()
        if key == ord('w'):
            kit.motor1.throttle = M1SPEED
            kit.motor2.throttle = M2SPEED
        elif key == ord('s'):
            kit.motor1.throttle = -M1SPEED
            kit.motor2.throttle = -M2SPEED
        elif key == ord('a'):
            kit.motor1.throttle = -M1SPEED
            kit.motor2.throttle = M2SPEED
        elif key == ord('d'):
            kit.motor1.throttle = M1SPEED
            kit.motor2.throttle = -M2SPEED
        elif key == ord('q'):
            kit.motor1.throttle = 0
            kit.motor2.throttle = 0
            break
        else:
            kit.motor1.throttle = 0
            kit.motor2.throttle = 0

        time.sleep(0.025)

if __name__ == "__main__":
    curses.wrapper(get_key)

