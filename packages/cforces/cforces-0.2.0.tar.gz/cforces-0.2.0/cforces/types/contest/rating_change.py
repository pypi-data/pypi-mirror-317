from datetime import datetime
from typing import Dict, Any

from ..object import Object


class RatingChange(Object):
    """Represents a participation of user in rated contest."""

    __slots__ = (
        "contest_id",
        "contest_name",
        "handle",
        "rank",
        "rating_update_time_seconds",
        "old_rating",
        "new_rating",
    )

    contest_id: int
    contest_name: str
    handle: str
    rank: int
    rating_update_time_seconds: int
    old_rating: int
    new_rating: int

    @property
    def rating_update_time(self) -> datetime:
        return datetime.fromtimestamp(self.rating_update_time_seconds)

    @staticmethod
    def from_dict(raw_data: Dict[str, Any]) -> "RatingChange":
        return RatingChange(**raw_data)
