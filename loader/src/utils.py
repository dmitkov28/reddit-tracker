from datetime import datetime


def current_date(today: datetime = datetime.now()) -> str:
    return today.strftime("%d-%m-%Y")


def build_path(bucket: str, athena_dir: str, date_dir: str = current_date()) -> str:
    return f"s3://{bucket}/{athena_dir}/{date_dir}"
