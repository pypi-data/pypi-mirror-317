from typing import List, Type, Dict, Any, Tuple
from cforces import errors
import pytest
import sys

if sys.version_info[0] == 3 and sys.version_info[1] < 11:
    from exceptiongroup import ExceptionGroup


TestData = Tuple[str, str, Type[errors.APIRequestLimitExceeded], Dict[str, Any]]
testdata_entries: List[TestData] = [
    (
        "count",
        "Field should be no more than 1000",
        errors.APIRequestLimitExceeded,
        {},
    ),
    (
        "count",
        "Field should be no more than 1000",
        errors.APIRequestLimitExceeded,
        {},
    ),
    (
        "blogEntryId",
        "Blog entry with id 93 not found",
        errors.BlogEntryNotFound,
        {"id": 93},
    ),
    (
        "contestId",
        "Contest with id 2051 has not started",
        errors.ContestHasNotStarted,
        {"id": 2051},
    ),
    (
        "contestId",
        "Field should contain long integer value",
        errors.InvalidParameter,
        {"comment": "long integer"},
    ),
    (
        "blogEntryId",
        "Field should contain long integer value",
        errors.InvalidParameter,
        {"comment": "long integer"},
    ),
    (
        "room",
        "Field should contain integer value",
        errors.InvalidParameter,
        {"comment": "integer"},
    ),
    (
        "count",
        "Field should contain integer value",
        errors.InvalidParameter,
        {"comment": "integer"},
    ),
    (
        "maxCount",
        "Field should contain integer value",
        errors.InvalidParameter,
        {"comment": "integer"},
    ),
    (
        "from",
        "Field should contain integer value",
        errors.InvalidParameter,
        {"comment": "integer"},
    ),
    (
        "participantTypes",
        "Unknown participant type: 'invalid'",
        errors.InvalidParticipantType,
        {"type": "invalid"},
    ),
    (
        "asManager",
        'Only contest managers can use "asManager" option',
        errors.NotAContestManager,
        {},
    ),
    ("count", "Field should be at least 1", errors.OneIndexed, {}),
    ("maxCount", "Field should be at least 1", errors.OneIndexed, {}),
    ("from", "Field should be at least 1", errors.OneIndexed, {}),
    (
        "problemsetName",
        "Problemset with name 'invalid' not found",
        errors.ProblemSetNotFound,
        {"name": "invalid"},
    ),
    ("handles", "Field should not be empty", errors.RequiredFieldMissing, {}),
    ("count", "Field should not be empty", errors.RequiredFieldMissing, {}),
    (
        "handles",
        "User with handle invalid not found",
        errors.UserNotFound,
        {"user": "invalid"},
    ),
    (
        "handle",
        "User with handle invalid not found",
        errors.UserNotFound,
        {"user": "invalid"},
    ),
]


@pytest.mark.parametrize("param,comment,exception,data", testdata_entries)
def test_exceptions(
    param: str,
    comment: str,
    exception: Type[errors.APIRequestLimitExceeded],
    data: Dict[str, Any],
) -> None:
    with pytest.raises(ExceptionGroup) as exc_info:
        raise errors.api_error(param + ": " + comment)

    assert len(exc_info.value.exceptions) == 1

    raised_exc: errors.GenericAPIError = exc_info.value.exceptions[0]
    assert isinstance(raised_exc, exception)
    assert raised_exc.param == param

    for key, value in data.items():
        assert hasattr(raised_exc, key)
        assert getattr(raised_exc, key) == value


@pytest.mark.parametrize("data1", testdata_entries)
@pytest.mark.parametrize("data2", testdata_entries)
def test_multi_exceptions(data1: TestData, data2: TestData) -> None:
    with pytest.raises(ExceptionGroup) as exc_info:
        raise errors.api_error(
            data1[0] + ": " + data1[1] + ";" + data2[0] + ": " + data2[1]
        )

    assert len(exc_info.value.exceptions) == 2

    raised_exc1: errors.GenericAPIError = exc_info.value.exceptions[0]
    raised_exc2: errors.GenericAPIError = exc_info.value.exceptions[1]
    assert isinstance(raised_exc1, data1[2])
    assert isinstance(raised_exc2, data2[2])
    assert raised_exc1.param == data1[0]
    assert raised_exc2.param == data2[0]

    for key, value in data1[3].items():
        assert hasattr(raised_exc1, key)
        assert getattr(raised_exc1, key) == value

    for key, value in data2[3].items():
        assert hasattr(raised_exc2, key)
        assert getattr(raised_exc2, key) == value


# TODO: Fix this
"""Those fail:
(
    "participantTypes",
    "Unknown participant type: 'true;invalid'",
    errors.InvalidParticipantType,
    {"type": "true;invalid"},
),
(
    "problemsetName",
    "Problemset with name 'true;invalid' not found",
    errors.ProblemSetNotFound,
    {"name": "true;invalid"},
),
(
    "handles",
    "User with handle true;invalid not found",
    errors.UserNotFound,
    {"handle": "true;invalid"},
),
(
    "handle",
    "User with handle true;invalid not found",
    errors.UserNotFound,
    {"handle": "true;invalid"},
),
"""
