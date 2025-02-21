import asyncio
import camera
import dht
import sensor

async def start(s: sensor.Sensor):
    await s.start()

async def main() -> None:
    Camera = camera.Camera()
    DHT = dht.DHT()

    sensors: list[sensor.Sensor] = [Camera, DHT]
    await asyncio.gather(*[start(sensor) for sensor in sensors])

if __name__ == "__main__":
    asyncio.run(main())

