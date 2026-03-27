from dataclasses import asdict, dataclass
from typing import Optional
from datetime import datetime


@dataclass()
class ThreadClean:
    id: str
    title: str
    selftext: Optional[str]
    created: float
    author: str
    permalink: str
    comments: Optional[int] = 0
    upvotes: Optional[int] = 0

    @property
    def created_dt(self):
        return datetime.fromtimestamp(self.created)

    @property
    def serialized(self):
        return asdict(self)


@dataclass
class Comment:
    id: str
    thread_id: str
    text: str
    created: float
    author: str
    permalink: str
    upvotes: Optional[int] = 0

    @property
    def created_dt(self):
        return datetime.fromtimestamp(self.created)

    @property
    def serialized(self):
        return asdict(self)


@dataclass
class CommentList:
    data: list[Comment]

    @property
    def serialized(self):
        return [asdict(comment) for comment in self.data]
