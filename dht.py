import asyncio
import time
import board
import adafruit_dht
import sensor
import pigpio
import threading


class DHT(sensor.Sensor):
    def __init__(self, stop_event):
        super().__init__()
        self.sensor = adafruit_dht.DHT11(board.D4, use_pulseio=False)
        self.stop_event = stop_event  # Store stop event

    async def start(self):
        while not self.stop_event.is_set():  # Check stop event
            try:
                self.sensor.measure()
                temperature_c = self.sensor.temperature
                humidity = self.sensor.humidity
                print(temperature_c, humidity)
            except RuntimeError as error:
                print(error.args[0])
                continue
            except Exception as error:
                self.sensor.exit()
                raise error

            await asyncio.sleep(5.0)

        print("DHT sensor stopping...")
        self.sensor.exit()  # Ensure sensor cleanup

def main() -> None:
    stop_event = threading.Event()
    d = DHT(stop_event)
    
    try:
        asyncio.run(d.start())  # Start async loop
    except KeyboardInterrupt:
        print("Stopping DHT sensor...")
        stop_event.set()

if __name__ == "__main__":
    main()

