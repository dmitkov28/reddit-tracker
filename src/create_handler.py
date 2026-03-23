import os

import httpx

from src import RedditClient
from src.utils.str_utils import clean_subreddit
from src.logger import logger

PROXY = os.getenv("HTTP_PROXY")


def create_handler():
    def handler(event: dict, context: dict):
        subreddit = clean_subreddit(event["subreddit"])

        with httpx.Client(timeout=30, proxy=PROXY) as client:
            client = RedditClient(client=client)
            try:
                return client.fetch_threads_for_subreddit(subreddit=subreddit)
            except Exception as e:
                logger.exception(str(e))

    return handler
