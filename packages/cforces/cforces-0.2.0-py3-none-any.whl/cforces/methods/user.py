from typing import List, Optional, Union

import cforces
from cforces import types, utils, errors


class User:
    async def user_blog_entries(
        self: "cforces.Client", handle: str
    ) -> List[types.BlogEntry]:
        """Retrieves blog entries of a specific user.

        :param handle: User's codeforces handle.
        :return: A list of blog entries.
        """
        return utils.parse_type_list(
            await self.api_call(
                "user.blogEntries",
                {"handle": handle},
            ),
            types.BlogEntry,
        )

    async def user_friends(
        self: "cforces.Client", only_online: bool = False
    ) -> List[str]:
        """Retrieves friends the friends of an authenticated user.

        :param only_online: If this parameter is true, then the API will only
            return the friends of the authenticated user who are online.
        :raises errors.Unauthorized: Raised if the user is not authenticated.
        :return: A list of handles.
        """
        if not self.authorized:
            raise errors.UserUnauthorized

        return await self.api_call(
            "user.friends",
            {"onlyOnline": only_online},
        )

    async def user_info(
        self: "cforces.Client",
        handles: Union[List[str], str],
        check_historic_handles: Optional[bool] = None,
    ) -> List[types.User]:
        """Retrieves the user information bounded to a list of handles.

        :param handles: List of handles. The API will not return information
            for more than 10000 handles.
        :param check_historic_handles: If this parameter is true, then the API
            will also use the information of any historic handle changes to
            search for users.
        :return: A list of users.
        """
        raw_handles: str
        if isinstance(handles, str):
            raw_handles = handles

        else:
            raw_handles = ";".join(handles)

        return utils.parse_type_list(
            await self.api_call(
                "user.info",
                {
                    "handles": raw_handles,
                    "checkHistoricHandles": check_historic_handles,
                },
            ),
            types.User,
        )

    async def user_rated_list(
        self: "cforces.Client",
        active_only: bool = False,
        include_retired: bool = False,
        contest_id: Optional[int] = None,
    ) -> List[types.User]:
        """Retrieves users that have been in, at least, one rated contest.

        :param active_only: Include only users that have participated in a
            rated contest during the last month.
        :param include_retired: Include users that have not been online during
            the last month.
        :param contest_id: ID of the contest. It's not the round number.
            It can be seen in the contest URL. For example, in the following
            `/contest/566/status <https://codeforces.com/contest/566/status>`,
            the **566** is the contest ID.
        :return: A list of users.
        """
        return utils.parse_type_list(
            await self.api_call(
                "user.ratedList",
                {
                    "activeOnly": active_only,
                    "includeRetired": include_retired,
                    "contestId": contest_id,
                },
            ),
            types.User,
        )

    async def user_rating(
        self: "cforces.Client", handle: str
    ) -> List[types.RatingChange]:
        """Retrieves the rating changes of a certain user over time.

        :param handle: User's codeforces handle.
        :return: A list of the user's rating changes.
        """
        return utils.parse_type_list(
            await self.api_call("contest.ratingChanges", {"handle": handle}),
            types.RatingChange,
        )

    async def user_status(
        self: "cforces.Client", handle: str, _from: int = 1, count: int = 10
    ) -> List[types.Submission]:
        """Retrieves the submissions of a specific user.

        :param handle: User's codeforces handle.
        :param _from: 1-based index of the first submission of the list that is
            going to be retrieved.
        :param count: Number of submissions to return.
        :return: A list of the user's submissions.
        """
        return utils.parse_type_list(
            await self.api_call(
                "user.status", {"handle": handle, "from": _from, "count": count}
            ),
            types.Submission,
        )
