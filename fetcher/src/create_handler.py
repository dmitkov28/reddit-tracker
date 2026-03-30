import os

import httpx

from src import RedditClient
from src.model import CommentList
from src.storer import S3Storer
from src.storer.storer import Storer
from src.utils.date_utils import Today
from src.utils.s3 import S3, CommentPartition, ThreadPartition
from src.logger import logger
from src.utils.str_utils import clean_subreddit

PROXY = os.getenv("HTTP_PROXY")
BUCKET = os.getenv("BUCKET")

if not BUCKET:
    raise ValueError("No bucket name provided")


def create_handler(storer: Storer = S3Storer(S3(bucket=BUCKET))):
    def handler(event: dict, context: dict):
        subreddit = clean_subreddit(event["subreddit"])

        today = Today()

        with httpx.Client(timeout=30, proxy=PROXY, follow_redirects=True) as client:
            client = RedditClient(client=client)

            try:
                comments = client.fetch_comments_for_subreddit(subreddit=subreddit)
                threads = client.fetch_threads_for_subreddit(subreddit=subreddit)
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
                    comments_for_thread = [
                        comment
                        for comment in comments
                        if comment.thread_id == thread.id
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

            except Exception as e:
                logger.exception(str(e))

    return handler
