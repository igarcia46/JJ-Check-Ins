from pathlib import Path
from datetime import datetime
import re

import cv2


class PhotoService:

    def __init__(self, photo_directory: str):
        self.photo_directory = Path(photo_directory)
        self.photo_directory.mkdir(parents=True, exist_ok=True)

    def save_photo(self, name: str, image) -> str:
        if image is None:
            raise ValueError("No image was provided.")

        safe_name = self._sanitize_name(name)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        file_name = f"{timestamp}_{safe_name}.jpg"

        file_path = self.photo_directory / file_name

        success = cv2.imwrite(str(file_path), image)

        if not success:
            raise IOError("Failed to save photo.")

        return str(file_path)

    def _sanitize_name(self, name: str) -> str:
        name = name.strip()

        if not name:
            return "visitor"

        name = re.sub(r"[^a-zA-Z0-9_-]", "_", name)

        return name