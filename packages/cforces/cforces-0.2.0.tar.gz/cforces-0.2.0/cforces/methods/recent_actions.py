from typing import List

import cforces
from cforces import types, utils


class RecentActions:
    async def recent_actions(
        self: "cforces.Client", max_count: int
    ) -> List[types.RecentAction]:
        """Retrieves public recent actions in the platform.

        :param max_count: Maximum count of recent actions to be retrieved.
            (Can be up to 100)
        :return: A list of recent actions.
        """
        return utils.parse_type_list(
            await self.api_call("recentActions", {"maxCount": max_count}),
            types.RecentAction,
        )
