from src.storer.storer import Storer
from src.utils.date_utils import Today
from src.utils.s3 import SubredditPartition
from src.reddit_client.client import RedditClient


def collect_subreddit(
    reddit_client: RedditClient, subreddit: str, storer: Storer, today: Today = Today()
):
    subreddit_metadata = reddit_client.fetch_subreddit_metadata(subreddit=subreddit)
    storer.store(
        partition=SubredditPartition(
            subreddit_id=subreddit_metadata.id,
            year=today.year,
            month=today.month,
            day=today.day,
        ),
        data=subreddit_metadata,
    )
    return subreddit_metadata
