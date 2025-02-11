import cv2
from flask import Flask, Response
import time
import sensor

class Camera(sensor.Sensor):
    def __init__(self):
        self.app = Flask(__name__)

        self.camera = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L2)
        self.camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.app.add_url_rule("/", "video_feed", self.video_feed)

    def generate_frames(self):
        while True:
            success, frame = self.camera.read()
            if not success:
                print("Error: Failed to capture frame")
                break
            _, buffer = cv2.imencode('.jpg', frame)
            if buffer is None:
                print("Error: Failed to encode frame")
                break
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    def video_feed(self):
        print("Starting video stream...")
        return Response(self.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

    def start(self):
        self.app.run(host="0.0.0.0", port=25565, threaded=True)
