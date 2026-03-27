import os

import httpx

from src import RedditClient
from src.storer import S3Storer
from src.utils.date_utils import Today
from src.utils.s3 import S3, Partition
from src.logger import logger
from src.utils.str_utils import clean_subreddit

PROXY = os.getenv("HTTP_PROXY")
BUCKET = os.getenv("BUCKET")


def create_handler():
    def handler(event: dict, context: dict):
        subreddit = clean_subreddit(event["subreddit"])
        if not BUCKET:
            raise ValueError("No bucket name provided")

        s3 = S3(bucket=BUCKET)
        storer = S3Storer(s3=s3)
        today = Today()

        with httpx.Client(timeout=30, proxy=PROXY) as client:
            client = RedditClient(client=client)

            try:
                threads = client.fetch_threads_for_subreddit(subreddit=subreddit)
                for thread in threads:
                    storer.store(
                        partition=Partition(
                            subreddit=subreddit,
                            year=today.year,
                            month=today.month,
                            day=today.day,
                            thread_id=thread.id,
                        ),
                        data=thread,
                    )

            except Exception as e:
                logger.exception(str(e))

    return handler
