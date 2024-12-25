from typing import Dict, Any, Optional
from urllib.parse import urljoin
from hashlib import sha512
import random
import string
import enum
import time

from aiohttp import ClientSession

from .methods import Methods
from .utils import cc2sc
from . import errors


class Client(Methods):
    __slots__ = ("params", "session", "api_key", "api_secret")
    params: Dict[str, Any]
    session: ClientSession

    api_key: Optional[str]
    api_secret: Optional[str]
    api_url: str = "https://codeforces.com/api/"

    def __init__(self, session: ClientSession) -> None:
        self.params = {"lang": "en"}
        self.session = session

        self.api_key = None
        self.api_secret = None

    def auth(self, api_key: str, api_secret: str) -> None:
        self.api_key = api_key
        self.api_secret = api_secret

    @property
    def authorized(self) -> bool:
        return self.api_key is not None and self.api_secret is not None

    async def api_call(
        self, method_name: str, params: Dict[str, Any], convert_case: bool = True
    ) -> Any:
        params.update(self.params)

        if self.authorized:
            params["apiKey"] = self.api_key
            params["time"] = int(time.time())

        raw_params: str = ""
        for k, v in sorted(params.items()):
            if not v:
                continue
            if isinstance(v, bool):
                v = int(v)
            elif isinstance(v, enum.Enum):
                v = v.value

            raw_params += ("&" if raw_params else "") + k + "=" + str(v)

        if self.authorized:
            rand: str = "".join(
                [random.choice(string.digits + string.ascii_letters) for x in range(6)]
            )

            base_api_sig: str = (
                rand + "/" + method_name + "?" + raw_params + "#" + self.api_secret
            )

            raw_params += (
                ("&" if raw_params else "")
                + "apiSig="
                + rand
                + sha512(base_api_sig.encode()).hexdigest()
            )

        url: str = urljoin(self.api_url, method_name) + "?" + raw_params
        async with self.session.get(url) as resp:
            raw_data: Dict[str, Any] = await resp.json()
            if raw_data["status"] == "FAILED":
                raise errors.api_error(raw_data["comment"])

        if convert_case and (isinstance(raw_data["result"], (dict, list))):
            return cc2sc(raw_data["result"])
        return raw_data["result"]
