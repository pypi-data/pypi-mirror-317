from typing import Optional

from httpx import AsyncClient


class AppInfo:
    __slots__ = ("api_id", "api_hash", "title", "short_name",)

    def __init__(self, api_id: int, api_hash: str, title: str, short_name: str) -> None:
        self.api_id = api_id
        self.api_hash = api_hash
        self.title = title
        self.short_name = short_name

    def __repr__(self) -> str:
        return (
            f"AppInfo(api_id={self.api_id!r}, api_hash={self.api_hash!r}, "
            f"title={self.title!r}, short_name={self.short_name!r})"
        )


class MyTelegram:
    __slots__ = ("_phone_number", "_api_host", "_random_hash", "_token",)

    def __init__(self, phone_number: str, api_host: str = "https://my.telegram.org") -> None:
        self._phone_number = phone_number
        self._api_host = api_host
        self._random_hash: Optional[str] = None
        self._token: Optional[str] = None

    async def send_code(self) -> None:
        async with AsyncClient() as client:
            resp = await client.post(f"{self._api_host}/auth/send_password", data={
                "phone": self._phone_number,
            })
            if resp.status_code != 200:
                raise ValueError(
                    f"Failed to send password: server responded with "
                    f"code {resp.status_code} and body \"{resp.text}\""
                )

            try:
                resp = resp.json()
            except ValueError:
                raise ValueError(
                    f"Failed to send password: server responded with "
                    f"code {resp.status_code} and body \"{resp.text}\""
                )

            if "random_hash" not in resp:
                raise ValueError(
                    f"Failed to send password: server did not return random_hash, response body: \"{resp}\""
                )

            self._random_hash = resp["random_hash"]

    async def login(self, password: str, remember: bool = True) -> None:
        if self._random_hash is None:
            raise ValueError("Random hash is not set, call send_code method first")

        async with AsyncClient() as client:
            resp = await client.post(f"{self._api_host}/auth/login", data={
                "phone": self._phone_number,
                "random_hash": self._random_hash,
                "password": password,
                "remember": "1" if remember else "0",
            })

            if resp.status_code != 200:
                raise ValueError(
                    f"Failed to login: server responded with code {resp.status_code} and body {resp.text}"
                )

            if "stel_token" not in resp.cookies:
                raise ValueError(f"Failed to login: server did not set token cookie")

            self._token = resp.cookies["stel_token"]
            self._random_hash = None

    async def get_app(self) -> AppInfo:
        if self._token is None:
            raise ValueError("Token is not set, call send_code and login methods first")

        async with AsyncClient() as client:
            resp = await client.get(f"{self._api_host}/apps", cookies={"stel_token": self._token})
            if resp.status_code != 200:
                raise ValueError(
                    f"Failed to get app: server responded with code {resp.status_code}"
                )

            body = resp.text.split("App api_id:")[1]
            body = body.split("<strong>")[1]
            api_id, body = body.split("</strong>", maxsplit=1)
            body = body.split("onclick=\"this.select();\">")[1]
            api_hash, body = body.split("</span>", maxsplit=1)

            # TODO: fix parsing of title and short name
            app_title = ""
            app_shortname = ""
            #body = body.split("name=\"app_title\"")[1]
            #body = body.split("value=\"")[1]
            #app_title, body = body.split("\"", maxsplit=1)
            #body = body.split("name=\"app_shortname\"")[1]
            #body = body.split("value=\"")[1]
            #app_shortname, body = body.split("\"", maxsplit=1)

            return AppInfo(int(api_id), api_hash, app_title, app_shortname)
