from datetime import datetime
import email
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
        email: str | None = None, # if email is not provided, it will be set to None, same for phone, reason, and photo_path
        phone: str | None = None,
        reason: str | None = None,
        photo_path: str | None = None,
    ) -> CheckInRecord: # returns the created CheckInRecord object

        name = name.strip()

        # validate that the name is not empty
        if not name:
            raise ValueError("Name is required.")

        # validate the email format if an email is provided
        if email:
            email = email.strip()
            self._validate_email(email)

        record = CheckInRecord(
            name=name,
            email=email, #TODO: check this works for when a user doesn't provide an email 
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

    # validates the email address format and raises a ValueError if it's invalid
    def _validate_email(self, email: str) -> None:
        if "@" not in email or "." not in email:
            raise ValueError("Please provide a valid email address (e.g., user@example.com)")