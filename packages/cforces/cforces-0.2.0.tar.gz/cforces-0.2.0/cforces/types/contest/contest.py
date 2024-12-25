from datetime import timedelta, datetime
from typing import Dict, Any, Optional

from ..object import Object
from ...enums import ContestType, ContestPhase


class Contest(Object):
    """Represents a contest on Codeforces."""

    __slots__ = (
        "id",
        "name",
        "type",
        "phase",
        "frozen",
        "duration_seconds",
        "freeze_duration_seconds",
        "start_time_seconds",
        "relative_time_seconds",
        "prepared_by",
        "website_url",
        "description",
        "difficulty",
        "kind",
        "icpc_region",
        "country",
        "city",
        "season",
    )

    id: int
    name: str
    type: ContestType
    phase: ContestPhase
    frozen: bool
    duration_seconds: Optional[int]
    freeze_duration_seconds: Optional[int]
    start_time_seconds: Optional[int]
    relative_time_seconds: Optional[int]
    prepared_by: Optional[str]
    website_url: Optional[str]
    description: Optional[str]
    difficulty: Optional[int]
    kind: Optional[str]
    icpc_region: Optional[str]
    country: Optional[str]
    city: Optional[str]
    season: Optional[str]

    def duration(self) -> timedelta:
        return timedelta(seconds=float(self.duration_seconds))

    def freeze_duration(self) -> timedelta:
        return timedelta(seconds=float(self.freeze_duration_seconds))

    def start_time(self) -> datetime:
        return datetime.fromtimestamp(float(self.start_time_seconds))

    def relative_time(self) -> timedelta:
        return timedelta(seconds=float(self.relative_time_seconds))

    @staticmethod
    def from_dict(raw_data: Dict[str, Any]) -> "Contest":
        raw_data["type"] = ContestType(raw_data["type"])
        raw_data["phase"] = ContestPhase(raw_data["phase"])
        return Contest(**raw_data)
