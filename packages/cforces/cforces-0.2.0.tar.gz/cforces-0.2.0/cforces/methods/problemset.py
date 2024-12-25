from typing import List, Dict, Any, Tuple, Optional, Union

import cforces
from cforces import types, utils


class ProblemSet:
    async def problemset_problems(
        self: "cforces.Client",
        tags: Optional[Union[List[str], str]] = None,
        problemset_name: Optional[str] = None,
    ) -> Tuple[List[types.Problem], List[types.ProblemStatistics]]:
        """Retrieves problems (and their statistics) from a problemset.

        :param tags: Problem tags.
        :param problemset_name: Short name of the problemset the problem belongs to.
        :return: A tuple of Problem's and ProblemStatistics's
        """
        raw_tags: Optional[str] = None
        if tags:
            if isinstance(tags, str):
                raw_tags = tags

            else:
                raw_tags = ";".join(tags)

        raw_problems: Dict[str, List[Dict[str, Any]]] = await self.api_call(
            "problemset.problems",
            {"tags": raw_tags, "problemsetName": problemset_name},
        )

        return utils.parse_type_list(
            raw_problems["problems"], types.Problem
        ), utils.parse_type_list(
            raw_problems["problemStatistics"], types.ProblemStatistics
        )

    async def problemset_recent_status(
        self: "cforces.Client", count: int = 10, problemset_name: Optional[str] = None
    ) -> List[types.Submission]:
        """Retrieves recent submissions from a problemset.

        :param count: Number of submissions to return.
        :param problemset_name: Short name of the problemset the problem belongs to.
        :return: A list of submissions belonging to the specified problemset.
        """
        return utils.parse_type_list(
            await self.api_call(
                "problemset.recentStatus",
                {"count": count, "problemsetName": problemset_name},
            ),
            types.Submission,
        )
