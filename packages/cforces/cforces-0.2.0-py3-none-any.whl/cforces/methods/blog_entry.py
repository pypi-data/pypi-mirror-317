from typing import List

import cforces
from cforces import types, utils


class BlogEntry:
    async def blog_entry_comments(
        self: "cforces.Client", blog_entry_id: int
    ) -> List[types.Comment]:
        """Retrieves every comment associated to a specific blog entry.

        :param blog_entry_id: ID of the target blog entry.
            It can be seen in the blog entry URL. For example:
            `/blog/entry/79 <https://codeforces/blog/entry/79>`_,
            where the **79** represents the ID of the blog entry.
        :return: The comments associated with the blog entry.
        """
        return utils.parse_type_list(
            await self.api_call("blogEntry.comments", {"blogEntryId": blog_entry_id}),
            types.Comment,
        )

    async def blog_entry_view(
        self: "cforces.Client", blog_entry_id: int
    ) -> types.BlogEntry:
        """Retrieves a blog entry object in its full version.

        :param blog_entry_id: ID of the target blog entry.
            It can be seen in the blog entry URL. For example:
            `/blog/entry/79 <https://codeforces/blog/entry/79>`_,
            where the **79** represents the ID of the blog entry.
        :return: A blog entry object in its full version.
        """
        return types.BlogEntry.from_dict(
            await self.api_call("blogEntry.view", {"blogEntryId": blog_entry_id})
        )
