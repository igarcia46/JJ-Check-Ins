import cv2


class CameraService:

    def __init__(self, camera_index: int = 0):
        self.camera_index = camera_index
        self.camera = None
        self.current_frame = None

    def start(self) -> None:
        if self.camera is not None and self.camera.isOpened():
            return

        self.camera = cv2.VideoCapture(self.camera_index)

        if not self.camera.isOpened():
            self.camera = None
            raise RuntimeError("Could not access camera.")

    def get_frame(self):
        if self.camera is None or not self.camera.isOpened():
            raise RuntimeError("Camera has not been started.")

        success, frame = self.camera.read()

        if not success:
            raise RuntimeError("Could not read frame from camera.")

        self.current_frame = frame

        return frame

    def capture_photo(self):
        if self.current_frame is None:
            raise RuntimeError("No camera frame available to capture.")

        return self.current_frame.copy()

    def release(self) -> None:
        if self.camera is not None:
            self.camera.release()
            self.camera = None
            self.current_frame = None