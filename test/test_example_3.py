from pyservice import action, Context, Organizer


def add_two_rollback(ctx: Context) -> Context:
    ctx["result"] -= 2
    return ctx


@action(expects=["n"], promises=["result"], rollback=add_two_rollback)
def add_two(ctx: Context) -> Context:
    number = ctx.get("n", 0)

    ctx["result"] = number + 2

    return ctx


@action()
def fail_context(ctx: Context) -> Context:
    ctx.fail("I don't like what I see here")
    raise Organizer.ContextFailed(fail_context)


def add_three_rollback(ctx: Context) -> Context:
    ctx["result"] -= 3
    return ctx


@action(expects=["result"], rollback=add_three_rollback)
def add_three(ctx: Context) -> Context:
    result = ctx["result"]

    ctx["result"] = result + 3

    return ctx


def test_can_run_functions():
    ctx = Context.make({"n": 4})
    organizer = Organizer([add_two, add_three, fail_context])
    result_ctx = organizer.run(ctx)

    assert ctx.is_failure
    assert result_ctx["result"] == 4
