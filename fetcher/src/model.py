from dataclasses import asdict, dataclass
from typing import Optional
from datetime import datetime


@dataclass
class BaseEntity:
    created: float

    @property
    def created_dt(self):
        return datetime.fromtimestamp(self.created)

    @property
    def serialized(self):
        return asdict(self)


@dataclass
class Subreddit(BaseEntity):
    id: str
    name: str
    subscribers: int


@dataclass
class ThreadClean(BaseEntity):
    id: str
    subreddit: str
    title: str
    selftext: Optional[str]
    author: str
    permalink: str
    comments: Optional[int] = 0
    upvotes: Optional[int] = 0
    downvotes: Optional[int] = 0


@dataclass
class Comment(BaseEntity):
    id: str
    thread_id: str
    text: str
    author: str
    permalink: str
    upvotes: Optional[int] = 0
    downvotes: Optional[int] = 0


@dataclass
class CommentList:
    data: list[Comment]

    @property
    def serialized(self):
        return [asdict(comment) for comment in self.data]
