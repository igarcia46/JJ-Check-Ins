from datetime import datetime
from models.CheckInRecord import CheckInRecord
from repositories.excel_repository import ExcelRepository

class CheckInService:

    # initializes the CheckInService with a repository for storing check-in records
    def __init__(self, repository: ExcelRepository):
        self.repository = repository

    # checks in a person by creating a CheckInRecord and saving it to the repository
    def check_in(
        self,
        name: str,
        phone: str | None = None,
        reason: str | None = None,
        photo_path: str | None = None,
    ) -> CheckInRecord: # returns the created CheckInRecord object

        name = name.strip()

        # validate that the name is not empty
        if not name:
            raise ValueError("Name is required.")

        record = CheckInRecord(
            name=name,
            phone=phone.strip() if phone else None,
            reason=reason.strip() if reason else None,
            check_in_time=datetime.now(),
            photo_path=photo_path,
        )

        self.repository.save(record)

        return record

    # gets all check-in records from the repository and returns them as a list of CheckInRecord objects
    def get_all_records(self) -> list[CheckInRecord]:
        return self.repository.get_all()
