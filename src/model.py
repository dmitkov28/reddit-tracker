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

    @property
    def created_dt(self):
        return datetime.fromtimestamp(self.created)

    @property
    def serialized(self):
        return asdict(self)
