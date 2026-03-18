import httpx

from src import RedditClient
from src.utils.str_utils import clean_subreddit


def create_handler():
    def handler(event: dict, context: dict):
        subreddit = clean_subreddit(event["subreddit"])

        with httpx.Client(timeout=30) as client:
            client = RedditClient()
            client.fetch_threads_for_subreddit(subreddit=subreddit)

    return handler
