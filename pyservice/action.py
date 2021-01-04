from abc import abstractmethod
from functools import wraps
from pyservice.context import Context
from typing import Callable, List, Optional


class ExpectedKeyNotFoundError(Exception):
    pass


class PromisedKeyNotFoundError(Exception):
    pass


def _verify_expected_keys(expected_keys: List[str], ctx_keys: List[str]) -> None:
    if not expected_keys:
        return

    set_expected_keys = set(expected_keys)
    set_ctx_keys = set(ctx_keys)
    expected_diff = set_expected_keys - set_ctx_keys

    if expected_diff:
        raise ExpectedKeyNotFoundError(f"Missing keys: {list(expected_diff)}")


def _verify_promised_keys(promised_keys: List[str], ctx_keys: List[str]) -> None:
    if not promised_keys:
        return

    promised_diff = set(promised_keys) - set(ctx_keys)

    if promised_diff:
        raise PromisedKeyNotFoundError(
            f"Promised keys not found: {list(promised_diff)}"
        )


def action(
        expects: List[str] = [],
        promises: List[str] = [],
        rollback: Optional[Callable] = None) -> Callable:
    def action_wrapper(f: Callable):
        @wraps(f)
        def decorated(ctx: Context, *args, **kwargs):
            _verify_expected_keys(expects, list(ctx.keys()))

            if ctx.is_failure or ctx.is_skipped:
                return ctx

            result = f(ctx, *args, **kwargs)

            _verify_promised_keys(promises, list(ctx.keys()))

            return result

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
