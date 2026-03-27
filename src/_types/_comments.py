from __future__ import annotations

from typing_extensions import TypedDict


class CommentData(TypedDict):
    id: str
    parent_id: str
    permalink: str
    ups: int
    body: str
    created: float
    author: str


class CommentChild(TypedDict):
    kind: str
    data: CommentData


class CommentListingData(TypedDict):
    after: str | None
    dist: int
    children: list[CommentChild]


class RedditCommentResponse(TypedDict):
    kind: str
    data: CommentListingData
