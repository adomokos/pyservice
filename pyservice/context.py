from typing import Any, Dict, Optional


class Context(dict):
    """ Wrapped dictionary carrying info between actions """

    def __init__(self, *arg, **kw):
        self.__success = True
        self.__skipped = False
        self.__message = None

    @property
    def is_failure(self) -> bool:
        return self.__success is False

    @property
    def is_success(self) -> bool:
        return self.__success

    @property
    def is_skipped(self) -> bool:
        return self.__skipped

    @property
    def message(self) -> Optional[str]:
        return self.__message

    def fail(self, msg: Optional[str] = None) -> None:
        if msg is not None:
            self.__message = msg

        self.__success = False

    def skip(self, msg: Optional[str] = None) -> None:
        if msg is not None:
            self.__message = msg

        self.__skipped = True

    @staticmethod
    def make(dict_value: Dict[str, Any] = {}) -> "Context":
        ctx = Context()
        ctx.update(dict_value)
        return ctx
