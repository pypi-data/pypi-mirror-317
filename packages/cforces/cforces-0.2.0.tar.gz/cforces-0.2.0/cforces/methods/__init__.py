from .recent_actions import RecentActions
from .problemset import ProblemSet
from .blog_entry import BlogEntry
from .contest import Contest
from .user import User


class Methods(RecentActions, ProblemSet, BlogEntry, Contest, User):
    pass


__all__ = ["Methods"]
