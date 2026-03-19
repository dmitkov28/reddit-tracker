import httpx

from src import RedditClient
from src.utils.str_utils import clean_subreddit
from src.logger import logger


def create_handler():
    def handler(event: dict, context: dict):
        subreddit = clean_subreddit(event["subreddit"])

        with httpx.Client(timeout=30) as client:
            client = RedditClient()
            try:
                client.fetch_threads_for_subreddit(subreddit=subreddit)
            except Exception as e:
                logger.exception(str(e))

    return handler
