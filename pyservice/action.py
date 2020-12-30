from abc import abstractmethod
from functools import wraps
from pyservice.context import Context
from typing import Callable


def action():
    def action_wrapper(f: Callable):
        @wraps(f)
        def decorated(ctx: Context, *args, **kwargs):
            if ctx.is_failure or ctx.is_skipped:
                return ctx

            return f(ctx, *args, **kwargs)

        return decorated

    return action_wrapper


def verify_context(func):
    """
    Guards the execution of the action, if the provided context
    is in a failure state or skipped, execution is stopped.
    """

    def wrapper(*args, **kwargs):
        (cls, ctx) = args

        if ctx.is_failure or ctx.is_skipped:
            return ctx

        return func(*args, **kwargs)

    return wrapper


class ActionMeta(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.execute = verify_context(cls.execute)


class Action(metaclass=ActionMeta):
    @abstractmethod
    def execute(self, ctx: Context) -> Context:
        pass

    def rollback(self, ctx: Context) -> Context:
        pass
