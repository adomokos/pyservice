from pyservice import action, Context, Organizer


@action(expects=["n"], promises=["result"])
def add_two(ctx: Context) -> Context:
    number = ctx.get("n", 0)

    ctx["result"] = number + 2

    return ctx


@action(expects=["result"])
def add_three(ctx: Context) -> Context:
    result = ctx["result"]

    ctx["result"] = result + 3

    return ctx


def test_can_run_functions():
    ctx = Context.make({"n": 4})
    organizer = Organizer([add_two, add_three])
    result_ctx = organizer.run(ctx)

    assert ctx.is_success
    assert result_ctx["result"] == 9
