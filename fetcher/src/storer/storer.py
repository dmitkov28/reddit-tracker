from typing import Protocol, Union

from src.model import CommentList, Subreddit, ThreadClean
from src.utils.s3 import S3, CommentPartition, SubredditPartition, ThreadPartition


class Storer(Protocol):
    def store(
        self,
        partition: Union[ThreadPartition, CommentPartition, SubredditPartition],
        data: Union[ThreadClean, CommentList, Subreddit],
    ): ...

    def store_sentinel(self): ...


class S3Storer(Storer):
    def __init__(self, s3: S3):
        self._s3 = s3

    def store(
        self,
        partition: Union[ThreadPartition, CommentPartition, SubredditPartition],
        data: Union[ThreadClean, CommentList, Subreddit],
    ):
        self._s3.put(key=str(partition), data=data.serialized)

    def store_sentinel(self):
        self._s3.put(key="_DONE", data=None)
