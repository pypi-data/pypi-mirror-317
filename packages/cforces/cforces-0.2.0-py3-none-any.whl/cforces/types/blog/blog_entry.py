from typing import List, Dict, Any, Optional
from datetime import datetime

from ..object import Object


class BlogEntry(Object):
    """Represents a Codeforces blog entry. May be in either short or full version."""

    __slots__ = (
        "id",
        "original_locale",
        "creation_time_seconds",
        "author_handle",
        "title",
        "content",
        "locale",
        "modification_time_seconds",
        "allow_view_history",
        "tags",
        "rating",
    )

    id: int
    original_locale: str
    creation_time_seconds: int
    author_handle: str
    title: str
    content: Optional[str]
    locale: str
    modification_time_seconds: int
    allow_view_history: bool
    tags: List[str]
    rating: int

    @property
    def creation_time(self) -> datetime:
        return datetime.fromtimestamp(self.creation_time_seconds)

    @property
    def modification_time(self) -> datetime:
        return datetime.fromtimestamp(self.modification_time_seconds)

    @property
    def short_version(self) -> bool:
        return self.content is None

    @staticmethod
    def from_dict(raw_data: Dict[str, Any]) -> "BlogEntry":
        return BlogEntry(**raw_data)
