import os

import httpx

from src.services import collect_subreddit, collect_comments, collect_threads
from src import RedditClient
from src.storer import S3Storer
from src.storer.storer import Storer
from src.utils.s3 import S3
from src.logger import logger
from src.utils.str_utils import clean_subreddit

PROXY = os.getenv("HTTP_PROXY")
BUCKET = os.getenv("BUCKET")

if not BUCKET:
    raise ValueError("No bucket name provided")


def create_handler(storer: Storer = S3Storer(S3(bucket=BUCKET))):
    def handler(event: dict, context: dict):
        subreddit = clean_subreddit(event["subreddit"])

        with httpx.Client(timeout=30, proxy=PROXY, follow_redirects=True) as client:
            client = RedditClient(client=client)

            try:
                threads = collect_threads(
                    reddit_client=client, storer=storer, subreddit=subreddit
                )
                collect_comments(
                    reddit_client=client,
                    storer=storer,
                    threads=threads,
                    subreddit=subreddit,
                )

                collect_subreddit(
                    reddit_client=client, storer=storer, subreddit=subreddit
                )

            except Exception as e:
                logger.exception(str(e))

            finally:
                storer.store_sentinel()

    return handler
