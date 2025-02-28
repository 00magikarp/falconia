import threading

import drive
import camera
import dht
import rotary
import sensor


class Rover:
    def __init__(self):
        pass

    def main() -> None:
        self.stop_event = threading.Event(self.stop_event)
        Camera = camera.Camera(self.stop_event)
        DHT = dht.DHT(self.stop_event)
        Rotary = rotary.Rotary(self.stop_event)
        Drive = drive.Drive(self.stop_event)

        sensors: list[sensor.Sensor] = [
                Camera,
                # DHT,
                Rotary,
                Drive
            ]
        threads = []
        for sensor in sensors:
            thread = threading.Thread(target=sensor.start))
            thread.start()
            threads.append(thread)

        try:
            while True:
                time.sleep(0.05)
        except KeyboardInterrupt:
            print("Stopping robot!")
            self.stop_event.set()

        for thread in threads:
            thread.join()

if __name__ == "__main__":
    r = Rover()
    r.main()

