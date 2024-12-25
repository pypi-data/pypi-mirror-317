from enum import Enum


class ProblemResultType(Enum):
    #: Results that may be subject to changes (by hacks, or the system tests).
    PRELIMINARY = "PRELIMINARY"
    #: Results that cannot change.
    FINAL = "FINAL"
