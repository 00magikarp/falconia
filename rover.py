import camera
import dht
import rotary
import sensor

def startAll(l: list[sensor.Sensor]):
    for s in l:
        threading.Thread(target=s.start())

def main() -> None:
    Camera = camera.Camera()
    DHT = dht.DHT()
    Rotary = rotary.Rotary()

    sensors: list[sensor.Sensor] = [
            Camera,
            # DHT,
            Rotary
        ]
    startAll(sensors)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit(0)

