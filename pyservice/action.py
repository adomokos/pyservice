from functools import wraps
from pyservice.context import Context
from typing import Callable, List, Optional

# Type declaration for Action
Action = Callable[[Context], Context]


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
    rollback: Optional[Action] = None,
) -> Callable:
    def action_wrapper(f: Callable):
        @wraps(f)
        def decorated(ctx: Context) -> Context:
            _verify_expected_keys(expects, list(ctx.keys()))

            if ctx.is_skipped:
                return ctx

            if ctx.is_failure:
                if rollback:
                    return rollback(ctx)
                else:
                    return ctx

            result = f(ctx)

            _verify_promised_keys(promises, list(ctx.keys()))

            return result

        return decorated

    return action_wrapper
