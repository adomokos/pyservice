from functools import wraps
from pyservice.context import Context
from typing import Callable


def action():
    def action_wrapper(f: Callable):
        @wraps(f)
        def decorated(ctx: Context, *args, **kwargs):
            if ctx.is_failure():
                return ctx

            return f(ctx, *args, **kwargs)

        return decorated
    return action_wrapper
