from typing import Dict, Any, Optional

from ..object import Object


class Member(Object):
    """Represents a member of a party."""

    __slots__ = ("handle", "name")

    handle: str
    name: Optional[str]

    @staticmethod
    def from_dict(raw_data: Dict[str, Any]) -> "Member":
        return Member(**raw_data)
