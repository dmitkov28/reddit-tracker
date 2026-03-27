from typing import Protocol

from src.model import ThreadClean
from src.utils.s3 import S3, Partition


class Storer(Protocol):
    def store(self, partition: Partition, data: ThreadClean): ...


class S3Storer(Storer):
    def __init__(self, s3: S3):
        self._s3 = s3

    def store(self, partition: Partition, data: ThreadClean):
        self._s3.put(key=str(partition), data=data.serialized)
