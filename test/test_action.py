import pytest
from pyservice import action, Action  # , Action
from pyservice import Context


@pytest.fixture
def ctx() -> Context:
    return Context.make()


@action()
def addTwo(ctx: Context) -> Context:
    n = ctx["n"]
    ctx["result"] = n + 2
    return ctx


@action()
def addThree(ctx: Context) -> Context:
    n = ctx["n"]
    ctx["result"] = n + 3
    return ctx


class AddTwo(Action):
    def execute(self, ctx):
        n = ctx["n"]
        ctx["result"] = n + 2
        return ctx


def test_fn__can_operate_on_context(ctx: Context) -> None:
    ctx["n"] = 3
    an_action = addTwo
    an_action(ctx)

    assert ctx["result"] == 5


def test_fn__will_fail_without_required_key(ctx: Context) -> None:
    ctx["x"] = 3

    with pytest.raises(KeyError):
        addTwo(ctx)


def test_fn__will_not_execute_if_in_failed_state(ctx: Context) -> None:
    ctx.fail()
    ctx["n"] = 3
    addTwo(ctx)

    assert "result" not in ctx.keys()


def test_class__can_use_instance_method(ctx: Context) -> None:
    ctx["n"] = 2
    a2 = AddTwo()
    a2.execute(ctx)
    assert ctx["result"] == 4


def test_class__execution_guarded_by_state_of_ctx(ctx: Context) -> None:
    ctx["n"] = 2
    ctx.fail()
    AddTwo().execute(ctx)

    assert "result" not in ctx.keys()
