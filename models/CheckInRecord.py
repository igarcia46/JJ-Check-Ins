from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class CheckInRecord:
    name: str
    email: Optional[str]
    phone: Optional[str]
    reason: Optional[str]

    check_in_time: datetime
    photo_path: Optional[str] = None