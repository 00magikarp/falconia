import cv2
from flask import Flask, Response
import threading

from sensor import Sensor

class Camera(Sensor):
    def __init__(self, stop_event):
        super().__init__()
        self.app = Flask(__name__)
        self.stop_event = stop_event  # Store stop event

        self.camera = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L2)
        self.camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 432)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 324)
        self.camera.set(cv2.CAP_PROP_FPS, 15)
        self.camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.camera.set(cv2.CAP_PROP_AUTOFOCUS, 0)

        self.app.add_url_rule("/", "video_feed", self.video_feed)

    def generate_frames(self):
        """Reads and serves frames from the camera, stopping when event is set."""
        while not self.stop_event.is_set():
            success, frame = self.camera.read()
            if not success:
                print("Error: Failed to capture frame")
                break
            _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

        print("Camera thread stopping...")
        self.camera.release()  # Ensure camera is released

    def video_feed(self):
        return Response(self.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

    def start(self):
        self.app.run(host="0.0.0.0", port=8554, threaded=True)  # Flask should run in a separate thread

if __name__ == "__main__":
    stop_event = threading.Event()
    c = Camera(stop_event)
    try:
        c.start()
    except KeyboardInterrupt:
        print("Stopping Camera...")
        stop_event.set()


