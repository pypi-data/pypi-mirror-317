from enum import Enum


class ParticipantType(Enum):
    #: Contestants who are participating live in the contest.
    CONTESTANT = "CONTESTANT"
    #: Contestants who are participating in practice mode in the contest.
    PRACTICE = "PRACTICE"
    #: Contestants who are participating in virtual mode in the contest.
    VIRTUAL = "VIRTUAL"
    #: Managers of the contest.
    MANAGER = "MANAGER"
    #: Contestants who don't meet the rating requirements for the contest.
    OUT_OF_COMPETITION = "OUT_OF_COMPETITION"
