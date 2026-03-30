from src.model import BaseEntity


import pytest

from datetime import datetime


@pytest.fixture
def timestamp():
    return datetime.fromisoformat("2026-03-28").timestamp()


@pytest.fixture
def base_entity(timestamp):
    return BaseEntity(
        created=timestamp,
    )


def test_created_dt_property(base_entity):
    assert base_entity.created_dt == datetime.fromisoformat("2026-03-28")


def test_serialized_property(base_entity, timestamp):
    assert base_entity.serialized == {"created": timestamp}
