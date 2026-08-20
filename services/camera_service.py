import cv2


class CameraService:

    def __init__(
        self,
        preferred_camera_index: int = 1,
        max_camera_index: int = 4,
    ):
        self.preferred_camera_index = preferred_camera_index
        self.max_camera_index = max_camera_index

        self.camera_index = None
        self.camera = None
        self.current_frame = None

    def start(self) -> None:
        if self.camera is not None and self.camera.isOpened():
            return

        camera_indexes = self._get_camera_indexes_to_try()

        for camera_index in camera_indexes:
            camera = cv2.VideoCapture(
                camera_index,
                cv2.CAP_DSHOW,
            )

            if not camera.isOpened():
                camera.release()
                continue

            success, frame = camera.read()

            if success and frame is not None:
                self.camera = camera
                self.camera_index = camera_index
                self.current_frame = frame

                print(
                    f"Camera started successfully "
                    f"using index {camera_index}"
                )

                return

            camera.release()

        raise RuntimeError(
            "No working camera could be found."
        )

    def get_frame(self):
        if self.camera is None or not self.camera.isOpened():
            raise RuntimeError(
                "Camera has not been started."
            )

        success, frame = self.camera.read()

        if not success:
            raise RuntimeError(
                "Could not read frame from camera."
            )

        self.current_frame = frame

        return frame

    def capture_photo(self):
        if self.current_frame is None:
            raise RuntimeError(
                "No camera frame available to capture."
            )

        return self.current_frame.copy()

    def release(self) -> None:
        if self.camera is not None:
            self.camera.release()

        self.camera = None
        self.camera_index = None
        self.current_frame = None

    def _get_camera_indexes_to_try(self) -> list[int]:
        indexes = [self.preferred_camera_index]

        for index in range(self.max_camera_index + 1):
            if index != self.preferred_camera_index:
                indexes.append(index)

        return indexes