from dataclasses import dataclass
from datetime import datetime, date as _date


@dataclass
class Today:
    year: int = datetime.now().year
    month: int = datetime.now().month
    day: int = datetime.now().day
    date: _date = datetime.today().date()

    def __eq__(self, value: datetime) -> bool:
        return self.date == value.date()
