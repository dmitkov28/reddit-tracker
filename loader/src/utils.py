from dataclasses import dataclass
from datetime import datetime


@dataclass
class Date:
    year: int = datetime.today().year
    month: int = datetime.today().month
    day: int = datetime.today().day


def build_path(bucket: str, athena_dir: str, date_dir: str = current_date()) -> str:
    return f"s3://{bucket}/{athena_dir}/{date_dir}"
