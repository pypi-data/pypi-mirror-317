from __future__ import annotations

from contextvars import ContextVar, Token
from typing import Dict, Optional, Union

JsonValue = Union[str, int, float, bool, None]
ContextJsonDict = Dict[str, JsonValue]


class ChalkContext:
    """
    An immutable context that can be accessed from Python resolvers.
    This context wraps a JSON-compatible dictionary or JSON string with type restrictions.

    The context is thread-local, so it can be accessed from multiple resolvers.
    """

    context_var: ContextVar[ContextJsonDict | None] = ContextVar("context_dict", default=None)

    @classmethod
    def _set_context(cls, context: ContextJsonDict | None) -> Token | None:
        if context is None:
            return None
        token = cls.context_var.set(context)
        return token

    @classmethod
    def get(cls, key: str, default: Optional[JsonValue] = None) -> Optional[JsonValue]:
        context_dict = cls.context_var.get()
        if context_dict is None:
            return default
        return context_dict.get(key, default)

    @classmethod
    def _reset(cls, token: Token | None):
        if token is None:
            return
        cls.context_var.reset(token)
