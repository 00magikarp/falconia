import cv2
from flask import Flask, Response
import time
import sensor
import threading

class Camera(sensor.Sensor):
    def __init__(self):
        self.app = Flask(__name__)

        self.camera = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L2)
        self.camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
        self.camera.set(cv2.CAP_PROP_FPS, 10)
        self.camera.set(cv2.CAP_PROP_BUFFERSIZE, 5)
        self.camera.set(cv2.CAP_PROP_AUTOFOCUS, 0)

        self.app.add_url_rule("/", "video_feed", self.video_feed)

    def generate_frames(self):
        while True:
            success, frame = self.camera.read()
            if not success:
                print("Error: Failed to capture frame")
                break
            _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
            if buffer is None:
                print("Error: Failed to encode frame")
                break
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    def video_feed(self):
        print("Starting video stream...")
        return Response(self.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

    async def start(self):
        thread = threading.Thread(target=self.app.run, kwargs={ "host": "0.0.0.0", "port": 8554, "threaded": True })
        thread.start()
        # self.app.run(host="0.0.0.0", port=8554, threaded=True)
