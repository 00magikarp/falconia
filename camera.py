import cv2
from flask import Flask, Response

from sensor import Sensor

class Camera(Sensor):
    def __init__(self):
        self.app = Flask(__name__)

        self.camera = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L2)
        self.camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 432)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 324)
        self.camera.set(cv2.CAP_PROP_FPS, 15)
        self.camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.camera.set(cv2.CAP_PROP_AUTOFOCUS, 0)

        self.app.add_url_rule("/", "video_feed", self.video_feed)

    def generate_frames(self):
        """Directly reads and serves frames from the camera."""
        while True:
            success, frame = self.camera.read()
            if not success:
                print("Error: Failed to capture frame")
                break
            _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    def video_feed(self):
        return Response(self.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

    def start(self):
        self.app.run(host="0.0.0.0", port=8554, threaded=False)  # No threading

if __name__ == "__main__":
    c = Camera()
    c.start()

