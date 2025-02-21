import asyncio
import time
import board
import adafruit_dht
import sensor
import DHT
import pigpio


class DHT(sensor.Sensor):
    def __init__(self):
        self.sensor = adafruit_dht.DHT11(board.D4, use_pulseio=False)

    async def start(self):
        while True:
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

def main() -> None:
    d = DHT()
    # asyncio.run(d.start())
    d.start()

if __name__ == "__main__":
    main()
