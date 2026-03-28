import pytest

from src.model import Comment, CommentList
from datetime import datetime


@pytest.fixture
def timestamp():
    return datetime.fromisoformat("2026-03-28").timestamp()


@pytest.fixture
def comment_list(timestamp):
    comments = [
        Comment(
            id=str(i),
            thread_id=str(i),
            text=f"test {i}",
            author=f"test {i}",
            permalink=f"test {i}",
            upvotes=10,
            created=timestamp,
        )
        for i in range(1, 3)
    ]
    return CommentList(data=comments)


def test_serialized_property(comment_list):
    assert comment_list.serialized == [
        {
            "created": 1774648800.0,
            "id": "1",
            "thread_id": "1",
            "text": "test 1",
            "author": "test 1",
            "permalink": "test 1",
            "upvotes": 10,
        },
        {
            "created": 1774648800.0,
            "id": "2",
            "thread_id": "2",
            "text": "test 2",
            "author": "test 2",
            "permalink": "test 2",
            "upvotes": 10,
        },
    ]
