import time
import board
import adafruit_dht
import sensor
import pigpio


class DHT(sensor.Sensor):
    def __init__(self):
        self.sensor = adafruit_dht.DHT11(board.D4, use_pulseio=False)

    def start(self):
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

            time.sleep(0.5)

        print("DHT sensor stopping...")
        self.sensor.exit()

if __name__ == "__main__":
    d = DHT()
    d.start()

