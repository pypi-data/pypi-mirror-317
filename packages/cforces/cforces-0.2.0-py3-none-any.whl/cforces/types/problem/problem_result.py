from datetime import datetime
from typing import Dict, Any, Optional

from ..object import Object
from ...enums import ProblemResultType


class ProblemResult(Object):
    """Represents a submission's results of a party for a problem."""

    __slots__ = (
        "points",
        "penalty",
        "rejected_attempt_count",
        "type",
        "best_submission_time_seconds",
    )

    points: float
    penalty: Optional[int]
    rejected_attempt_count: int
    type: ProblemResultType
    best_submission_time_seconds: Optional[int]

    @property
    def best_submission_time(self) -> datetime:
        return datetime.fromtimestamp(float(self.best_submission_time_seconds))

    @staticmethod
    def from_dict(raw_data: Dict[str, Any]) -> "ProblemResult":
        raw_data["type"] = ProblemResultType(raw_data["type"])
        return ProblemResult(**raw_data)
