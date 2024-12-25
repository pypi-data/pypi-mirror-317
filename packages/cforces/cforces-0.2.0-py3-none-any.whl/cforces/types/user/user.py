from datetime import datetime
from typing import Dict, Optional, Union

from ..object import Object


class User(Object):
    """Represents a Codeforces user."""

    __slots__ = (
        "handle",
        "email",
        "vk_id",
        "open_id",
        "first_name",
        "last_name",
        "country",
        "city",
        "organization",
        "contribution",
        "rank",
        "rating",
        "max_rank",
        "max_rating",
        "last_online_time_seconds",
        "registration_time_seconds",
        "friend_of_count",
        "avatar",
        "title_photo",
    )

    handle: str
    email: Optional[str]
    vk_id: Optional[str]
    open_id: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    country: Optional[str]
    city: Optional[str]
    organization: Optional[str]
    contribution: int
    rank: str
    rating: int
    max_rank: str
    max_rating: int
    last_online_time_seconds: int
    registration_time_seconds: int
    friend_of_count: int
    avatar: str
    title_photo: str

    @property
    def last_online_time(self) -> datetime:
        return datetime.fromtimestamp(self.last_online_time_seconds)

    @property
    def registration_time(self) -> datetime:
        return datetime.fromtimestamp(self.registration_time_seconds)

    @staticmethod
    def from_dict(raw_data: Dict[str, Union[int, str]]) -> "User":
        return User(**raw_data)
