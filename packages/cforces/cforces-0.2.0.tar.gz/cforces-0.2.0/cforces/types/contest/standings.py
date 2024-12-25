from typing import List, Dict, Any

from ..problem.problem import Problem
from .ranklist_row import RanklistRow
from .contest import Contest
from ..object import Object


class Standings(Object):
    """Non-API-Compliant Codeforces Type"""

    __slots__ = ("contest", "problems", "rows")

    contest: Contest
    problems: List[Problem]
    rows: List[RanklistRow]

    @staticmethod
    def from_dict(raw_data: Dict[str, Any]) -> "Standings":
        raw_data["contest"] = Contest.from_dict(raw_data["contest"])

        ranklist_rows: List[RanklistRow] = []
        problems: List[Problem] = []

        for raw_ranklist_row in raw_data["rows"]:
            ranklist_rows.append(RanklistRow.from_dict(raw_ranklist_row))

        for raw_problem in raw_data["problems"]:
            problems.append(Problem.from_dict(raw_problem))

        raw_data["rows"] = ranklist_rows
        raw_data["problems"] = problems

        return Standings(**raw_data)
