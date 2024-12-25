from enum import Enum


# TODO: Recognize ranks by rating
class Rank(Enum):
    #: User with a rating between or equal to: 0 and 1199
    NEWBIE = "newbie"
    #: User with a rating between or equal to: 1200 and 1399
    PUPIL = "pupil"
    #: User with a rating between or equal to: 1400 and 1599
    SPECIALIST = "specialist"
    #: User with a rating between or equal to: 1600 and 1899
    EXPERT = "expert"
    #: User with a rating between or equal to: 1900 and 2099
    CANDIDATE_MASTER = "candidate master"
    #: User with a rating between or equal to: 2100 and 2299
    MASTER = "master"
    #: User with a rating between or equal to: 2300 and 2399
    INTERNATIONAL_MASTER = "international master"
    #: User with a rating between or equal to: 2400 and 2599
    GRANDMASTER = "grandmaster"
    #: User with a rating between or equal to: 2600 and 2999
    INTERNATIONAL_GRANDMASTER = "international grandmaster"
    #: User with a rating between or equal to: 3000 and 3999
    LEGENDARY_GRANDMASTER = "legendary grandmaster"
    #: User with a rating greater or equal to: 4000
    TOURIST = "tourist"
