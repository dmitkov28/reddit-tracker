from dataclasses import dataclass
from datetime import datetime
from typing import Literal


@dataclass
class Date:
    year: int = datetime.today().year
    month: int = datetime.today().month
    day: int = datetime.today().day


def build_path(
    bucket: str,
    athena_dir: str,
    query_type: Literal["subreddits", "threads", "comments"],
    date: Date = Date(),
) -> str:

    return f"s3://{bucket}/{athena_dir}/{query_type}/year={date.year}/month={date.month}/day={date.day}"
