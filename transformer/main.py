from datetime import datetime
import logging
import os
from typing import Literal

import boto3

SUBREDDITS_QUERY = """
SELECT 
    id,
    name,
    subscribers
FROM subreddits
WHERE year = year(CURRENT_DATE)
  AND month = month(CURRENT_DATE)
  AND day = day(CURRENT_DATE)
  AND CAST(from_unixtime(created) AS DATE) >= CURRENT_DATE - INTERVAL '2' DAY
"""

COMMENTS_QUERY = """
SELECT 
    id,
    thread_id,
    text,
    author,
    permalink,
    upvotes,
    downvotes,
    CAST(from_unixtime(created) AS DATE) AS created_date
FROM comments
WHERE year = year(CURRENT_DATE)
  AND month = month(CURRENT_DATE)
  AND day = day(CURRENT_DATE)
  AND CAST(from_unixtime(created) AS DATE) >= CURRENT_DATE - INTERVAL '2' DAY;
"""

THREADS_QUERY = """
    SELECT 
    id,
    title,
    selftext AS text,
    author,
    permalink,
    comments,
    upvotes,
    downvotes,
    CAST(from_unixtime(created) AS DATE) AS created_date
FROM reddit.threads
WHERE year = year(CURRENT_DATE)
  AND month = month(CURRENT_DATE)
  AND day = day(CURRENT_DATE)
  AND CAST(from_unixtime(created) AS DATE) >= CURRENT_DATE - INTERVAL '2' DAY
"""


def build_unload_query(
    query: str,
    output_path: str,
    output_format: Literal["PARQUET", "JSON", "CSV"] = "PARQUET",
    output_compression: Literal["SNAPPY", "ZSTD", "BROTLI", "GZIP"] = "SNAPPY",
):
    return f"""
        UNLOAD ({query})
        TO '{output_path}'
        WITH (
            format = '{output_format}',
            compression = '{output_compression}'
        )
    """


logger = logging.getLogger()
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))


def lambda_handler(event: dict, context: dict):
    DATABASE = os.environ["ATHENA_DB"]
    BUCKET = os.environ["BUCKET"]

    logger.info("Starting transformation", extra={"bucket": BUCKET})

    DATE_PREFIX = datetime.now().strftime("%d-%m-%Y")

    OUTPUT = f"s3://{BUCKET}/athena/{DATE_PREFIX}"

    athena_client = boto3.client("athena", region_name="eu-central-1")

    queries = [
        ("subreddits", SUBREDDITS_QUERY),
        ("comments", COMMENTS_QUERY),
        ("threads", THREADS_QUERY),
    ]

    for name, query in queries:
        unload_query = build_unload_query(query, output_path=f"{OUTPUT}/{name}/")
        response = athena_client.start_query_execution(
            QueryString=unload_query,
            QueryExecutionContext={"Database": DATABASE},
            ResultConfiguration={"OutputLocation": OUTPUT},
            ResultReuseConfiguration={
                "ResultReuseByAgeConfiguration": {
                    "Enabled": True,
                    "MaxAgeInMinutes": 60,
                }
            },
        )
        query_id = response["QueryExecutionId"]
        logger.info(
            "Query started",
            extra={"table": name, "query_execution_id": query_id},
        )
