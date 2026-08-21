from pathlib import Path
import cv2
from pygrabber.dshow_graph import FilterGraph


class CameraService:

    MAX_CAMERA_INDEX = 5

    def __init__(self):
        self.camera = None
        self.camera_index = None
        self.current_frame = None
        self.camera_names = []

        self.log_path = (
            Path.home()
            / "Documents"
            / "Jonathan Jennings Visitor Check-In"
            / "camera_debug.txt"
        )

    def _log(self, message: str):
        self.log_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            self.log_path,
            "a",
            encoding="utf-8"
        ) as file:
            file.write(message + "\n")

    def discover_cameras(self):
        self._log("Starting camera scan...")
        available_cameras = []

        try:
            self.camera_names = FilterGraph().get_input_devices()
            self._log(
                "DirectShow devices: "
                + ", ".join(self.camera_names)
            )
        except Exception as error:
            self.camera_names = []
            self._log(f"Could not read camera names: {error}")

        for index in range(self.MAX_CAMERA_INDEX):
            self._log(f"Testing camera index {index}")

            camera = cv2.VideoCapture(
                index,
                cv2.CAP_DSHOW
            )

            if not camera.isOpened():
                self._log(
                    f"Index {index}: could not open"
                )
                camera.release()
                continue

            success, frame = camera.read()

            if not success:
                self._log(
                    f"Index {index}: opened but could not read frame"
                )
                camera.release()
                continue

            if frame is None:
                self._log(
                    f"Index {index}: returned empty frame"
                )
                camera.release()
                continue

            height, width = frame.shape[:2]

            self._log(
                f"Index {index}: SUCCESS - "
                f"{width}x{height}"
            )

            available_cameras.append(index)
            camera.release()

        return available_cameras

    def get_camera_name(self, camera_index):
        if camera_index < len(self.camera_names):
            name = self.camera_names[camera_index].strip()
            if name:
                return name

        return f"Camera {camera_index + 1}"

    def start(self, camera_index=None):
        self.release()

        if camera_index is None:
            available_cameras = self.discover_cameras()
            if not available_cameras:
                raise RuntimeError(
                    "No working camera could be found."
                )
            camera_index = available_cameras[0]

        self._log(f"Starting camera index {camera_index}")
        camera = cv2.VideoCapture(
            camera_index,
            cv2.CAP_DSHOW
        )

        if not camera.isOpened():
            camera.release()
            raise RuntimeError(
                f"Camera {camera_index + 1} could not be opened."
            )

        success, frame = camera.read()
        if not success or frame is None:
            camera.release()
            raise RuntimeError(
                f"Camera {camera_index + 1} did not return an image."
            )

        self.camera = camera
        self.camera_index = camera_index
        self.current_frame = frame

    def get_frame(self):
        if self.camera is None or not self.camera.isOpened():
            raise RuntimeError("Camera is not available.")

        success, frame = self.camera.read()
        if not success or frame is None:
            raise RuntimeError("Could not read from the camera.")

        self.current_frame = frame
        return frame

    def capture_photo(self):
        if self.current_frame is None:
            raise RuntimeError("No camera image is available.")

        return self.current_frame.copy()

    def release(self):
        if self.camera is not None:
            self.camera.release()

        self.camera = None
        self.camera_index = None
        self.current_frame = None
