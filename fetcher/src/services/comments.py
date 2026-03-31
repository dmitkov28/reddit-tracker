from src.model import CommentList, ThreadClean
from src.storer.storer import Storer
from src.utils.date_utils import Today
from src.utils.s3 import CommentPartition
from src.reddit_client.client import RedditClient


def collect_comments(
    reddit_client: RedditClient,
    threads: list[ThreadClean],
    subreddit: str,
    storer: Storer,
    today: Today = Today(),
):
    comments = reddit_client.fetch_comments_for_subreddit(subreddit=subreddit)
    for thread in threads:
        comments_for_thread = [
            comment for comment in comments if comment.thread_id == thread.id
        ]
        comment_list = CommentList(data=comments_for_thread)
        if comment_list.data:
            storer.store(
                partition=CommentPartition(
                    subreddit=subreddit,
                    thread_id=thread.id,
                    year=today.year,
                    month=today.month,
                    day=today.day,
                ),
                data=comment_list,
            )
    return comments
