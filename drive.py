import time
import curses
from adafruit_motorkit import MotorKit

# Initialize the motor hat
kit = MotorKit()

# Configuration
MAX_SPEED = 1.0  # Maximum throttle (range: 0 to 1)
ACCELERATION_STEP = 0.05  # How fast it speeds up
DECELERATION_STEP = 0.1  # Ensure both motors decelerate at the same rate
UPDATE_RATE = 0.05  # Update interval (lower = smoother, higher = more responsive)

# Current speed levels
motor1_speed = 0.0
motor2_speed = 0.0

def motor_control(stdscr):
    global motor1_speed, motor2_speed
    curses.cbreak()
    curses.halfdelay(1)  # Reduce delay for key holds (1 = 100ms)
    stdscr.nodelay(True)  # Do not block waiting for user input
    stdscr.keypad(True)
    stdscr.clear()
    stdscr.addstr("Use arrow keys to control motors. Press 'q' to exit.\n")

    while True:
        key = stdscr.getch()

        # Determine target speeds
        if key == curses.KEY_UP:
            target_speed_m1 = MAX_SPEED
            target_speed_m2 = -MAX_SPEED
        elif key == curses.KEY_DOWN:
            target_speed_m1 = -MAX_SPEED
            target_speed_m2 = MAX_SPEED
        elif key == curses.KEY_LEFT:
            target_speed_m1 = MAX_SPEED
            target_speed_m2 = MAX_SPEED
        elif key == curses.KEY_RIGHT:
            target_speed_m1 = -MAX_SPEED
            target_speed_m2 = -MAX_SPEED
        else:
            target_speed_m1 = 0
            target_speed_m2 = 0

        # Apply the same acceleration and deceleration logic to both motors
        for i, (current_speed, target_speed) in enumerate([(motor1_speed, target_speed_m1), (motor2_speed, target_speed_m2)]):
            if current_speed < target_speed:
                current_speed = min(current_speed + ACCELERATION_STEP, target_speed)
            elif current_speed > target_speed:
                current_speed = max(current_speed - DECELERATION_STEP, target_speed)
            if i == 0:
                motor1_speed = current_speed
            else:
                motor2_speed = current_speed

        motor1_speed = round(motor1_speed, 3)
        motor2_speed = round(motor2_speed, 3)

        # Apply the speeds to the motors
        kit.motor1.throttle = motor1_speed
        kit.motor2.throttle = motor2_speed

        # Display status
        stdscr.clear()
        stdscr.addstr("Use arrow keys to control motors. Press 'q' to exit.\n")
        stdscr.addstr(f"Motor 1 Speed: {motor1_speed}\n")
        stdscr.addstr(f"Motor 2 Speed: {motor2_speed}\n")
        stdscr.refresh()

        # Exit on 'q' key
        if key == ord('q'):
            break

        time.sleep(UPDATE_RATE)

    # Ensure motors fully stop when exiting
    kit.motor1.throttle = 0
    kit.motor2.throttle = 0

if __name__ == "__main__":
    curses.wrapper(motor_control)