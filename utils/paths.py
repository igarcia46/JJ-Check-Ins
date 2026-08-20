from pathlib import Path


APP_FOLDER_NAME = "Jonathan Jennings Visitor Check-In"


def get_data_directory() -> Path:
    data_directory = (
        Path.home()
        / "Documents"
        / APP_FOLDER_NAME
    )

    data_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    return data_directory


def get_excel_path() -> Path:
    return get_data_directory() / "check_ins.xlsx"


def get_photo_directory() -> Path:
    photo_directory = get_data_directory() / "photos"

    photo_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    return photo_directory