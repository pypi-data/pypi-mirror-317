"""Context class for keeping track of the conversation state in Redis."""

from typing import Any, NamedTuple

from redis import asyncio as redis

from lego.models import ReprEnum
from lego.settings import RedisConnection


class SessionInfo(NamedTuple):
    """Session information tuple."""

    access_token: str
    session_id: str
    ttl: float


class RedisContext:
    """Redis context with get, set, and delete methods."""

    def __init__(
        self,
        conversation_id: str,
        connection: RedisConnection,
        from_url: bool = True,
    ) -> None:
        ## `redis.from_url` may require proper handling with
        ## `urllib.parse.unquote_plus` which is currently not implemented
        ## in the code.
        self.redis = (
            redis.from_url(connection.url())
            if from_url
            else redis.Redis(**connection.model_dump())
        )
        self.redon = self.redis.json()
        self.convid = conversation_id

    async def init(self) -> None:
        """Initialize the conversation context."""
        await self.redon.set(self.convid, "$", {}, nx=True)

    async def session_info(self) -> tuple[str, str, float] | None:
        """
        Return the session info.

        Returns: NamedTuple(access_token, session_id, ttl).
        """
        session_id = await self.redon.get(self.convid, "$.session_id")
        if not session_id:
            return None

        token = await self.redon.get(self.convid, "$.access_token")
        if not token:
            raise KeyError("Access token is missing.")

        return SessionInfo(
            access_token=token,
            session_id=session_id[0],
            ttl=await self.redis.ttl(self.convid),
        )

    async def set_session(
        self,
        access_token: str,
        session_id: str,
        expires_in: float | None = None,
    ) -> None:
        """
        Set the session info.

        Args:
            :param access_token: The access token for OAuth2.0 authentication.
            :param session_id: The session ID to distinguish among sessions.
            :param expires_in: If provided, the expiration time in seconds.
                Will be rounded to the integer by discarding the decimal part.
        """
        await self.redon.set(self.convid, "$.session_id", session_id)
        await self.redon.set(self.convid, "$.access_token", access_token)
        if expires_in is not None and expires_in > 0:
            await self.redis.expire(self.convid, int(expires_in))

    async def get(  # type: ignore[misc]
        self,
        key: str | ReprEnum | None = None,
        fallback_value: Any = None,
        label: str = "state",
    ) -> Any:
        """Get a key-value pair from the conversation state."""
        uri = f"$.{label}.{key}" if key else f"$.{label}"
        result = await self.redon.get(self.convid, uri)
        return result[0] if result else fallback_value

    async def set_(
        self,
        key: str | ReprEnum,
        value: Any,  # type: ignore[misc]
        list_append: bool = False,
        dict_to_add: str | None = None,
        label: str = "state",
    ) -> None:
        """
        Set a key-value pair in the conversation state.

        Args:
            :param key: The key to set the value.
            :param value: The value to set.
            :param list_append: If True, the value will be appended to the list
            :param dict_to_add: If not None, the value will be added to the specified dict
            :param label: The label to set the key-value pair.
        """
        if not label.isalnum():
            raise ValueError("Label must be alphanumeric.")
        if list_append and dict_to_add:
            raise ValueError(
                "Conflicting arguments: `list_append` and `dict_to_add`."
            )
        uri = ["", ""]
        uri[0] = f"$.{label}.{key}"

        if list_append:
            potential_list = await self.get(key, label=label)
            if potential_list is None:
                await self.redon.set(self.convid, uri[0], [])
            elif not isinstance(potential_list, list):
                raise ValueError(f"Not a list under the key {key}.")
            await self.redon.arrappend(self.convid, uri[0], value)
            return

        if dict_to_add:
            uri[0] = f"$.{label}.{dict_to_add}.{key}"
            uri[1] = f"$.{label}.{dict_to_add}"
            potential_dict = await self.get(dict_to_add, label=label)
            if potential_dict is None:
                await self.redon.set(self.convid, uri[1], {})
            elif not isinstance(potential_dict, dict):
                raise ValueError(f"Not a dict under the key {dict_to_add}.")

        await self.redon.set(self.convid, uri[0], value)

    async def count(self, key: str | ReprEnum, label: str = "state") -> int:
        """Update the counter under the `key`."""
        if counter := await self.get(key, label=label):
            if not isinstance(counter, int):
                raise TypeError("Counter is not an integer.")
        else:
            await self.set_(key, 1, label=label)
        res = await self.redon.numincrby(self.convid, f"$.{label}.{key}", 1)
        return res[0]

    async def delete(
        self,
        key: str | ReprEnum | None = None,
        label: str | None = None,
    ) -> None:
        """
        Delete a key-value pair from the conversation state.

        If the key is not found, it will do nothing.
        """
        if key is None and label is None:
            await self.redis.delete(self.convid)
            return

        if label is None:
            label = "state"

        if await self.get(key, label=label):
            await self.redon.delete(self.convid, f"$.{label}.{key}")

    async def close(self) -> None:
        """Close the Redis connection."""
        await self.redis.aclose()
