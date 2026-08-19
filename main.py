import cv2

from services.camera_service import CameraService
from services.photo_service import PhotoService


camera_service = CameraService()
photo_service = PhotoService("data/photos")

try:
    camera_service.start()

    while True:
        frame = camera_service.get_frame()

        cv2.imshow("Camera Test", frame)

        key = cv2.waitKey(1)

        if key == ord(" "):
            photo = camera_service.capture_photo()

            path = photo_service.save_photo(
                name="Test Visitor",
                image=photo,
            )

            print(f"Photo saved: {path}")

        elif key == ord("q"):
            break

finally:
    camera_service.release()
    cv2.destroyAllWindows()