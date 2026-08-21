from pathlib import Path
import cv2


class CameraService:

    def __init__(self):
        self.camera = None
        self.camera_index = None
        self.current_frame = None

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

    def start(self):
        self._log("Starting camera scan...")

        for index in range(5):
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

            self.camera = camera
            self.camera_index = index
            self.current_frame = frame

            return

        raise RuntimeError(
            "No working camera could be found."
        )