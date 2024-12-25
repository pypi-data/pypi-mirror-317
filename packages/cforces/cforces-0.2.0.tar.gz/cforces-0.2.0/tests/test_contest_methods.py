from typing import Dict, Union, Optional

from cforces.methods.contest import Contest
import pytest


@pytest.mark.parametrize("contest_id", [1])
@pytest.mark.parametrize("as_manager", [None, False])
@pytest.mark.parametrize("handle", [None, "x93bd0"])
@pytest.mark.parametrize("_from", [None, 1])
@pytest.mark.parametrize("count", [None, 1])
async def test_contest_status(
    contest_id: int,
    as_manager: bool,
    handle: str,
    _from: Optional[int],
    count: Optional[int],
    helper,
) -> None:
    params: Dict[str, Union[int, str, bool]] = helper.params_from_tuple(
        ("contestId", "asManager", "handle", "from", "count"),
        (contest_id, as_manager, handle, _from, count),
    )

    helper.client.expect_api_call("contest.status", params, [])
    assert (
        await Contest.contest_status(
            helper.client, contest_id, as_manager, handle, _from, count
        )
    ) == []


def test_contest_list() -> None:
    pass


def test_contest_standings() -> None:
    pass


def test_contest_hacks() -> None:
    pass


def test_contest_rating_changes() -> None:
    pass
