import asyncio
import camera
import sensor

async def start(s: sensor.Sensor):
    s.start()

camera = camera.Camera();

asyncio.run(start(camera))
