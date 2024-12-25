from datetime import datetime, timedelta
from typing import Dict, Any, Optional

from .problem import Problem
from ..object import Object
from ..user.party import Party
from ...enums import TestSet, Verdict


class Submission(Object):
    """Represents a submission."""

    __slots__ = (
        "id",
        "contest_id",
        "creation_time_seconds",
        "relative_time_seconds",
        "problem",
        "author",
        "programming_language",
        "verdict",
        "testset",
        "passed_test_count",
        "time_consumed_millis",
        "memory_consumed_bytes",
        "points",
    )

    id: int
    contest_id: Optional[int]
    creation_time_seconds: int
    relative_time_seconds: int
    problem: Problem
    author: Party
    programming_language: str
    verdict: Verdict
    testset: TestSet
    passed_test_count: int
    time_consumed_millis: int
    memory_consumed_bytes: int
    points: Optional[float]

    @property
    def creation_time(self) -> datetime:
        return datetime.fromtimestamp(self.creation_time_seconds)

    @property
    def relative_time(self) -> timedelta:
        return timedelta(seconds=self.relative_time_seconds)

    @property
    def time_consumed(self) -> timedelta:
        return timedelta(microseconds=self.time_consumed_millis)

    @staticmethod
    def from_dict(raw_data: Dict[str, Any]) -> "Submission":
        if "verdict" in raw_data:
            raw_data["verdict"] = Verdict(raw_data["verdict"])

        raw_data["problem"] = Problem.from_dict(raw_data["problem"])
        raw_data["author"] = Party.from_dict(raw_data["author"])
        raw_data["testset"] = TestSet(raw_data["testset"])
        return Submission(**raw_data)
