from typing import Any, Dict


class Context(dict):
    """ Wrapped dictionary carrying info between actions """

    def __init__(self, *arg, **kw):
        self.__success = True

    @property
    def is_failure(self: 'Context') -> bool:
        return self.__success is False

    @property
    def is_success(self: 'Context') -> bool:
        return self.__success

    def fail(self: 'Context') -> None:
        self.__success = False

    @staticmethod
    def make(dict_value: Dict[str, Any] = {}) -> 'Context':
        ctx = Context()
        ctx.update(dict_value)
        return ctx
