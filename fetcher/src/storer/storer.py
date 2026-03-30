from typing import Protocol, Union

from src.model import CommentList, ThreadClean
from src.utils.s3 import S3, CommentPartition, ThreadPartition


class Storer(Protocol):
    def store(
        self,
        partition: Union[ThreadPartition, CommentPartition],
        data: Union[ThreadClean, CommentList],
    ): ...


class S3Storer(Storer):
    def __init__(self, s3: S3):
        self._s3 = s3

    def store(
        self,
        partition: Union[ThreadPartition, CommentPartition],
        data: Union[ThreadClean, CommentList],
    ):
        self._s3.put(key=str(partition), data=data.serialized)
