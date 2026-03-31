from src.utils.date_utils import Today
from src.utils.s3 import ThreadPartition
from src.reddit_client.client import RedditClient
from src.storer.storer import Storer


def collect_threads(
    reddit_client: RedditClient,
    storer: Storer,
    subreddit: str,
    today: Today = Today(),
):
    threads = reddit_client.fetch_threads_for_subreddit(subreddit=subreddit)
    for thread in threads:
        storer.store(
            partition=ThreadPartition(
                subreddit=subreddit,
                year=today.year,
                month=today.month,
                day=today.day,
                thread_id=thread.id,
            ),
            data=thread,
        )
    return threads
