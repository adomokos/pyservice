from pyservice import action
from pyservice import Context
from pyservice import Organizer2


def add_two_rollback(ctx: Context) -> Context:
    n = ctx["n"]

    result = ctx.get("result", n)

    ctx.update(result=result - 2)
    return ctx


@action(expects=["n"], rollback=add_two_rollback)
def add_two_with_rollback(ctx: Context) -> Context:
    n = ctx["n"]

    result = ctx.get("result", n)

    ctx.update(result=result + 2)
    return ctx


@action(expects=["n"])
def add_two(ctx: Context) -> Context:
    n = ctx["n"]

    result = ctx.get("result", n)

    ctx.update(result=result + 2)
    return ctx


def add_three_rollback(ctx: Context) -> Context:
    ctx["result"] -= 3
    return ctx


@action(promises=["result"], rollback=add_three_rollback)
def add_three_with_rollback(ctx: Context) -> Context:
    ctx["result"] += 3
    return ctx


@action(promises=["result"])
def add_three(ctx: Context) -> Context:
    ctx["result"] += 3
    return ctx


@action()
def fail_context(ctx: Context) -> Context:
    ctx.fail("Something went wrong...")
    raise Organizer2.ContextFailed(fail_context)


@action()
def skip_rest(ctx: Context) -> Context:
    ctx.skip("No need to run the rest")
    return ctx


organizer = Organizer2([add_two, add_three])
