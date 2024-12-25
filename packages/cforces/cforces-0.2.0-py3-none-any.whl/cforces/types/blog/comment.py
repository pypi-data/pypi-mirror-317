from datetime import datetime
from typing import Dict, Any, Optional

from ..object import Object


class Comment(Object):
    """Represents a comment."""

    __slots__ = (
        "id",
        "creation_time_seconds",
        "commentator_handle",
        "locale",
        "text",
        "parent_comment_id",
        "rating",
    )

    id: int
    creation_time_seconds: int
    commentator_handle: str
    locale: str
    text: str
    parent_comment_id: Optional[int]
    rating: int

    @property
    def creation_time(self) -> datetime:
        return datetime.fromtimestamp(self.creation_time_seconds)

    @staticmethod
    def from_dict(raw_data: Dict[str, Any]) -> "Comment":
        return Comment(**raw_data)
