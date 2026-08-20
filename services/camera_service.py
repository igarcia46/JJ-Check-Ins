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
        self._log("\n==============================")
        self._log("Starting FULL camera scan...")
        self._log("==============================")

        working_cameras = []

        for index in range(5):
            self._log(f"Testing camera index {index}")

            camera = cv2.VideoCapture(
                index,
                cv2.CAP_DSHOW,
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
                f"Index {index}: SUCCESS - {width}x{height}"
            )

            working_cameras.append(index)

            camera.release()

        self._log(
            f"Working camera indexes: {working_cameras}"
        )

        # After diagnosis, use the first working camera
        if not working_cameras:
            raise RuntimeError(
                "No working camera could be found."
            )

        selected_index = working_cameras[0]

        self._log(
            f"Opening camera index {selected_index} for application"
        )

        self.camera = cv2.VideoCapture(
            selected_index,
            cv2.CAP_DSHOW,
        )

        if not self.camera.isOpened():
            raise RuntimeError(
                f"Could not reopen camera index {selected_index}."
            )

        self.camera_index = selected_index

        success, frame = self.camera.read()

        if not success or frame is None:
            self.release()

            raise RuntimeError(
                f"Could not read from camera index {selected_index}."
            )

        self.current_frame = frame