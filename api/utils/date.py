from datetime import datetime
from fastapi import HTTPException, status


def str_to_date(date: str) -> datetime:
    try:
        return datetime.strptime(date, "%d-%m-%Y")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format. Date format should be DD-MM-YYYY",
        )
