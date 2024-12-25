from typing import Callable, Dict, List, Optional
import sys

from .base import CodeforcesException

if sys.version_info[0] == 3 and sys.version_info[1] < 11:
    from exceptiongroup import ExceptionGroup


class GenericAPIError(CodeforcesException):
    __slots__ = ("param", "comment")
    param: str
    comment: Optional[str]

    def __init__(
        self, param: str, comment: Optional[str], exc_text: Optional[str] = None
    ) -> None:
        if not exc_text:
            exc_text = (
                "Parameter '"
                + param
                + "' raised the following error: '"
                + (comment or "no error")
                + "'"
            )

        super().__init__(exc_text)
        self.param = param
        self.comment = comment


class APIRequestLimitExceeded(GenericAPIError):
    __slots__ = ("maximum",)
    maximum: int

    def __init__(self, param: str, maximum: int) -> None:
        super().__init__(
            param,
            None,
            "API Limit exceeded, parameter '"
            + param
            + "' only allows integer values up to '"
            + str(maximum)
            + "'",
        )

        self.maximum = maximum


class BlogEntryNotFound(GenericAPIError):
    __slots__ = ("id",)
    id: int

    def __init__(self, param: str, entry_id: int):
        super().__init__(
            param, None, "Blog entry with id '" + str(entry_id) + "' not found"
        )

        self.id = entry_id


class ContestHasNotStarted(GenericAPIError):
    __slots__ = ("id",)

    def __init__(self, param: str, contest_id: int) -> None:
        super().__init__(
            param, None, "Contest id:" + str(contest_id) + " has not started yet!"
        )

        self.id = contest_id


class InvalidCredentials(GenericAPIError):
    def __init__(self, param: str) -> None:
        super().__init__(param, None, "Invalid credentials!")


class InvalidParameter(GenericAPIError):
    def __init__(self, param: str, expected: str) -> None:
        super().__init__(
            param,
            expected,
            "The API didn't accept the input of the parameter"
            + param
            + "' because of the format. The API expected a[n] '"
            + expected
            + "'",
        )


class InvalidParticipantType(GenericAPIError):
    __slots__ = ("type",)
    type: str

    def __init__(self, param: str, participant_type: str) -> None:
        super().__init__(
            param, None, "Invalid participant type: '" + participant_type + "'"
        )

        self.type = participant_type


class NotAContestManager(GenericAPIError):
    def __init__(self, param: str) -> None:
        super().__init__(param, None, "Logged user is not a contest manager!")


class OneIndexed(GenericAPIError):
    pass


class ProblemSetNotFound(GenericAPIError):
    __slots__ = ("name",)
    name: str

    def __init__(self, param: str, problemset_name: str) -> None:
        super().__init__(
            param, None, "Problem set with name '" + problemset_name + "' not found!"
        )

        self.name = problemset_name


class RequiredFieldMissing(GenericAPIError):
    def __init__(self, param: str):
        super().__init__(
            param, None, "Parameter '" + param + "' is required for this API endpoint!"
        )


class UserNotFound(GenericAPIError):
    __slots__ = ("user",)
    user: str

    def __init__(self, param: str, user: str) -> None:
        super().__init__(param, None, "User with handle '" + user + "' not found!")
        self.user = user


class UserUnauthorized(GenericAPIError):
    def __init__(self, param: str) -> None:
        super().__init__(param, None, "User unauthorized!")


def _api_key_exc(param: str, about: str) -> Optional[GenericAPIError]:
    if about == "Incorrect API key":
        return InvalidCredentials(param)
    return None


def _as_manager_exc(param: str, _: str) -> GenericAPIError:
    return NotAContestManager(param)


def _blog_entry_exc(param: str, about: str) -> Optional[GenericAPIError]:
    if about.endswith("not found"):
        return BlogEntryNotFound(param, int(about[:-10].rsplit(" ", 1)[1]))
    return None


def _contest_id_exc(param: str, about: str) -> Optional[GenericAPIError]:
    if about.endswith("has not started"):
        return ContestHasNotStarted(param, int(about[:-16].rsplit(" ", 1)[1]))
    if about.startswith("Rating changes are unavailable"):
        return ContestHasNotStarted(param, -1)
    return None


def _handle_exc(param: str, about: str) -> Optional[GenericAPIError]:
    if about.endswith(" not found"):
        return UserNotFound(param, about[:-10].rsplit(" ", 1)[1])
    return None


def _handles_exc(param: str, about: str) -> Optional[GenericAPIError]:
    if about.endswith(" not found"):
        return UserNotFound(param, about[:-10].rsplit(" ", 1)[1])
    return None


def _only_online_exc(param: str, _: str) -> Optional[GenericAPIError]:
    return UserUnauthorized(param)


def _participant_type_exc(param: str, about: str) -> Optional[GenericAPIError]:
    if about.startswith("Unknown"):
        return InvalidParticipantType(param, about.rsplit(" ", 1)[1][1:-1])
    return None


def _problemset_name_exc(param: str, about: str) -> Optional[GenericAPIError]:
    if about.endswith(" not found"):
        return ProblemSetNotFound(param, about[:-10].rsplit(" ", 1)[1][1:-1])
    return None


error_handlers: Dict[str, Callable[[str, str], Optional[GenericAPIError]]] = {
    "apiKey": _api_key_exc,
    "asManager": _as_manager_exc,
    "blogEntryId": _blog_entry_exc,
    "contestId": _contest_id_exc,
    "handle": _handle_exc,
    "handles": _handles_exc,
    "onlyOnline": _only_online_exc,
    "participantTypes": _participant_type_exc,
    "problemsetName": _problemset_name_exc,
}


def api_error(comments: str) -> ExceptionGroup[GenericAPIError]:
    exceptions: List[GenericAPIError] = []
    for comment in comments.split(";"):
        if not comment:
            continue

        param: str
        about: str

        param, about = comment.split(": ", 1)
        words: List[str] = about.split(" ")

        if words[0] == "Field":
            if words[2] == "contain":
                exceptions.append(InvalidParameter(param, " ".join(words[3:-1])))
                continue

            if words[4] == "least":
                exceptions.append(OneIndexed(param, about))
                continue

            if words[4] == "more":
                exceptions.append(APIRequestLimitExceeded(param, int(words[-1])))
                continue

            if words[4] == "empty":
                exceptions.append(RequiredFieldMissing(param))
                continue

            exceptions.append(GenericAPIError(param, about))

        elif param in error_handlers:
            exc: Optional[GenericAPIError] = error_handlers[param](param, about)
            exceptions.append(exc or GenericAPIError(param, about))

        else:
            exceptions.append(GenericAPIError(param, about))

    return ExceptionGroup("An API error was raised", exceptions)
