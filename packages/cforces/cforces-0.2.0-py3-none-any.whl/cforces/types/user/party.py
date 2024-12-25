from datetime import datetime
from typing import List, Dict, Any, Optional

from ..object import Object
from ..user.member import Member
from ...enums import ParticipantType


class Party(Object):
    """Represents a party, participating in a contest."""

    __slots__ = (
        "contest_id",
        "members",
        "participant_type",
        "team_id",
        "team_name",
        "ghost",
        "room",
        "start_time_seconds",
    )

    contest_id: Optional[int]
    members: List[Member]
    participant_type: ParticipantType
    team_id: Optional[int]
    team_name: Optional[str]
    ghost: bool
    room: Optional[int]
    start_time_seconds: Optional[int]

    @property
    def start_time(self) -> datetime:
        return datetime.fromtimestamp(float(self.start_time_seconds))

    @staticmethod
    def from_dict(raw_data: Dict[str, Any]) -> "Party":
        members: List[Member] = []
        for raw_member in raw_data["members"]:
            members.append(Member.from_dict(raw_member))
        raw_data["members"] = members

        raw_data["participant_type"] = ParticipantType(raw_data["participant_type"])
        return Party(**raw_data)
