from typing import List, Dict, Any, Optional

from ..object import Object
from ...enums import ProblemType


class Problem(Object):
    """Represents a problem."""

    __slots__ = (
        "contest_id",
        "problemset_name",
        "index",
        "name",
        "type",
        "points",
        "rating",
        "tags",
    )

    contest_id: Optional[int]
    problemset_name: Optional[str]
    index: str
    name: str
    type: ProblemType
    points: Optional[float]
    rating: Optional[int]
    tags: List[str]

    @staticmethod
    def from_dict(raw_data: Dict[str, Any]) -> "Problem":
        raw_data["type"] = ProblemType(raw_data["type"])
        return Problem(**raw_data)
