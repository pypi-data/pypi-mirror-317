from enum import Enum


# TODO: Implement __getitem__ (TestSet[n] -> TESTS_n)


class TestSet(Enum):
    #: Samples testset data shown in problem statement.
    SAMPLES = "SAMPLES"
    #: Light tests used before tests on certain contest types.
    PRETESTS = "PRETESTS"
    #: Problem system tests.
    TESTS = "TESTS"
    #: Undocumented (TODO)
    CHALLENGES = "CHALLENGES"

    #: Testset #1
    TESTS1 = "TESTS1"
    #: Testset #2
    TESTS2 = "TESTS2"
    #: Testset #3
    TESTS3 = "TESTS3"
    #: Testset #4
    TESTS4 = "TESTS4"
    #: Testset #5
    TESTS5 = "TESTS5"
    #: Testset #6
    TESTS6 = "TESTS6"
    #: Testset #7
    TESTS7 = "TESTS7"
    #: Testset #8
    TESTS8 = "TESTS8"
    #: Testset #9
    TESTS9 = "TESTS9"
    #: Testset #10
    TESTS10 = "TESTS10"
