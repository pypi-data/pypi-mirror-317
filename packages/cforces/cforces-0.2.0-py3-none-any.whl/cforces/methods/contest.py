from typing import List, Optional, Union

import cforces
from cforces import types, utils, enums


class Contest:
    async def contest_hacks(
        self: "cforces.Client", contest_id: int, as_manager: Optional[bool] = None
    ) -> List[types.Hack]:
        """Fetches hacks created during a contest.

        Full information about hacks is available only after some time after
        the contest ends. During the contest, a user can only view his own
        hacks.

        :param contest_id: ID of the contest. It's not the round number.
            It can be seen in the contest URL. For example, in the following
            `/contest/566/status <https://codeforces.com/contest/566/status>`,
            the **566** is the contest ID.
        :param as_manager: If set to true, the response will contain
            information available to contest managers. Otherwise, the response
            will contain only the information available to the participants.
            You must be a contest manager to use it.
        :return: A list of hacks made during the requested contest.
        """
        return utils.parse_type_list(
            await self.api_call(
                "contest.hacks", {"contestId": contest_id, "asManager": as_manager}
            ),
            types.Hack,
        )

    async def contest_list(
        self: "cforces.Client", gym: Optional[bool] = None
    ) -> List[types.Contest]:
        """Retrieves the list of upcoming/finished contests.

        :param gym: If true, then gym contests are returned.
            Otherwise, regular contests are returned.
        :return: A list containing upcoming/finished contests.
        """
        return utils.parse_type_list(
            await self.api_call("contest.list", {"gym": gym}), types.Contest
        )

    async def contest_rating_changes(
        self: "cforces.Client", contest_id: int
    ) -> List[types.RatingChange]:
        """Retrieves rating changes during a specific contest.

        :param contest_id: ID of the contest. It's not the round number.
            It can be seen in the contest URL. For example, in the following
            `/contest/566/status <https://codeforces.com/contest/566/status>`,
            the **566** is the contest ID.
        :return: A list of rating changes that happened in the requested
            contest.
        """
        return utils.parse_type_list(
            await self.api_call("contest.ratingChanges", {"contestId": contest_id}),
            types.RatingChange,
        )

    async def contest_standings(
        self: "cforces.Client",
        contest_id: int,
        as_manager: bool = False,
        _from: Optional[int] = None,
        count: Optional[int] = None,
        handles: Optional[Union[List[str], str]] = None,
        room: Optional[int] = None,
        show_unofficial: bool = False,
        participant_types: Optional[List[Union[enums.ParticipantType, str]]] = None,
    ) -> types.Standings:
        """Retrieves standings of a specific contest.

        This can return the standings of specific users using the `handles`
        parameter.

        :param contest_id: ID of the contest. It's not the round number.
            It can be seen in the contest URL. For example, in the following
            `/contest/566/status <https://codeforces.com/contest/566/status>`,
            the **566** is the contest ID.
        :param as_manager: If set to true, the response will contain
            information available to contest managers. Otherwise, the response
            will contain only the information available to the participants.
            You must be a contest manager to use it.
        :param _from: 1-based index of the first standings row that is going
            to be fetched. (Note: If you request specific users using `handles`,
            then this will indicate from where it should start searching)
        :param count: Number of rows to return.
        :param handles: List of handles. The API will not return information
            for more than 10000 handles.
        :param room: If specified, then only participants from this room will
            be shown in the result.
        :param show_unofficial: If true, then all participants are shown.
            Otherwise, only official contestants are shown.
        :param participant_types: List of allowed participant types. Only
            participants with the specified types will be returned.
        :return: A list of standings of the requested contest.
        """
        raw_handles: Optional[str] = None
        if handles:
            if isinstance(handles, str):
                raw_handles = handles

            else:
                raw_handles = ";".join(handles)

        return types.Standings.from_dict(
            await self.api_call(
                "contest.standings",
                {
                    "contestId": contest_id,
                    "asManager": as_manager,
                    "from": _from,
                    "count": count,
                    "handles": raw_handles,
                    "room": room,
                    "showUnofficial": show_unofficial,
                    "participantTypes": (
                        ",".join(
                            [
                                (
                                    pt.value
                                    if isinstance(pt, enums.ParticipantType)
                                    else pt
                                )
                                for pt in participant_types
                            ]
                        )
                        if participant_types
                        else None
                    ),
                },
            )
        )

    async def contest_status(
        self: "cforces.Client",
        contest_id: int,
        as_manager: bool = False,
        handle: Optional[str] = None,
        _from: Optional[int] = None,
        count: Optional[int] = None,
    ) -> List[types.Submission]:
        """Retrieves submissions for a specific contest.

        It can also fetch submissions of a specific user in the contest if the
        parameter `handle` is used.

        :param contest_id: ID of the contest. It's not the round number.
            It can be seen in the contest URL. For example, in the following
            `/contest/566/status <https://codeforces.com/contest/566/status>`,
            the **566** is the contest ID.
        :param as_manager: If set to true, the response will contain
            information available to contest managers. Otherwise, the response
            will contain only the information available to the participants.
            You must be a contest manager to use it.
        :param handle: If specified, returns the submissions in this contest of
            the user with this handle.
        :param _from: 1-based index of the first standings row that is going
            to be retrieved.
        :param count: Number of rows to return.
        :return: A list of submission made during the requested contest.
        """
        return utils.parse_type_list(
            await self.api_call(
                "contest.status",
                {
                    "contestId": contest_id,
                    "asManager": as_manager,
                    "handle": handle,
                    "from": _from,
                    "count": count,
                },
            ),
            types.Submission,
        )
