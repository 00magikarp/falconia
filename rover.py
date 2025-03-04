import threading

import drive
import camera
# import dht
import mpu
import rotary
import sensor


class Rover:
    def __init__(self):
        pass

    def main() -> None:
        Camera = camera.Camera()
        # DHT = dht.DHT()
        Rotary = rotary.Rotary()
        MPU = mpu.MPU()
        Drive = drive.Drive()

        sensors: list[sensor.Sensor] = [
                Camera,
                # DHT,
                Rotary,
                MPU,
                Drive
            ]
        threads = []
        for sensor in sensors:
            thread = threading.Thread(target=sensor.start)
            thread.start()
            threads.append(thread)

        try:
            while True:
                time.sleep(0.05)
        except KeyboardInterrupt:
            print("Stopping robot!")

        for thread in threads:
            thread.join()

if __name__ == "__main__":
    r = Rover()
    r.main()

