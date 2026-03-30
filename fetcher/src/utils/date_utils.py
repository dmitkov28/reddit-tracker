from dataclasses import dataclass
from datetime import datetime


@dataclass
class Today:
    year: int = datetime.now().year
    month: int = datetime.now().month
    day: int = datetime.now().day
