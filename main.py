from repositories.excel_repository import ExcelRepository
from services.check_in_service import CheckInService


repository = ExcelRepository("data/check_ins.xlsx")
check_in_service = CheckInService(repository)

record = check_in_service.check_in(
    name="Jose Smith",
    email="jose@email.com",
    phone="317-555-4321",
    reason="Picking up child",
)

print(record)