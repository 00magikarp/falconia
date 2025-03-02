import smbus
import time
import math

# MPU6050 Registers
MPU6050_ADDR = 0x68
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43

class MPU:
    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)  # Wake up MPU6050

        # Noise thresholds
        self.ACCEL_THRESHOLD = 0.1
        self.GYRO_THRESHOLD = 1.0

        # Bias values
        self.ACCEL_BIAS = [0.0, 0.0, 1.0]
        self.GYRO_BIAS = [0.0, 0.0, 0.0]

    def read_word(self, reg):
        high = self.bus.read_byte_data(MPU6050_ADDR, reg)
        low = self.bus.read_byte_data(MPU6050_ADDR, reg + 1)
        value = (high << 8) + low
        return value - 65536 if value >= 32768 else value

    def get_accel_gyro(self):
        ax = self.read_word(ACCEL_XOUT_H) / 16384.0 - self.ACCEL_BIAS[0]
        ay = self.read_word(ACCEL_XOUT_H + 2) / 16384.0 - self.ACCEL_BIAS[1]
        az = self.read_word(ACCEL_XOUT_H + 4) / 16384.0 - self.ACCEL_BIAS[2]
        gx = self.read_word(GYRO_XOUT_H) / 131.0 - self.GYRO_BIAS[0]
        gy = self.read_word(GYRO_XOUT_H + 2) / 131.0 - self.GYRO_BIAS[1]
        gz = self.read_word(GYRO_XOUT_H + 4) / 131.0 - self.GYRO_BIAS[2]

        # Apply noise threshold filtering
        ax = ax if abs(ax) > self.ACCEL_THRESHOLD else 0.0
        ay = ay if abs(ay) > self.ACCEL_THRESHOLD else 0.0
        az = az if abs(az) > self.ACCEL_THRESHOLD else 0.0
        gx = gx if abs(gx) > self.GYRO_THRESHOLD else 0.0
        gy = gy if abs(gy) > self.GYRO_THRESHOLD else 0.0
        gz = gz if abs(gz) > self.GYRO_THRESHOLD else 0.0

        return ax, ay, az, gx, gy, gz

    def calculate_angle(self, ax, ay, az):
        roll = math.atan2(ay, az) * 180 / math.pi
        pitch = math.atan2(-ax, math.sqrt(ay**2 + az**2)) * 180 / math.pi
        return roll, pitch

    def start(self):
        prev_time = time.time()
        vel_x = vel_y = vel_z = 0.0
        pos_x = pos_y = pos_z = 0.0
        angle_x = angle_y = angle_z = 0.0

        while True:
            curr_time = time.time()
            dt = curr_time - prev_time
            prev_time = curr_time

            ax, ay, az, gx, gy, gz = self.get_accel_gyro()
            roll, pitch = self.calculate_angle(ax, ay, az)

            vel_x += ax * 9.81 * dt
            vel_y += ay * 9.81 * dt
            vel_z += az * 9.81 * dt

            pos_x += vel_x * dt
            pos_y += vel_y * dt
            pos_z += vel_z * dt

            angle_x += gx * dt
            angle_y += gy * dt
            angle_z += gz * dt

            print(f"Gyro: gx={gx:.2f}°/s, gy={gy:.2f}°/s, gz={gz:.2f}°/s")
            print(f"Angle: Roll={roll:.2f}°, Pitch={pitch:.2f}°")
            print(f"Angle mod 90: Roll={(roll)%90:.2f}, Pitch={(pitch)%90:.2f}")
            print("-" * 40)
            time.sleep(0.5)

        print("MPU6050 stopping...")


if __name__ == "__main__":
    mpu = MPU()
    mpu.start()

