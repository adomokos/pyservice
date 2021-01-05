import pytest
from pyservice import action  # , Action
from pyservice import (
    Context,
    ExpectedKeyNotFoundError,
    PromisedKeyNotFoundError,
)
from .test_doubles import add_two


@pytest.fixture
def ctx() -> Context:
    return Context.make()


def test_fn__can_operate_on_context(ctx: Context) -> None:
    ctx["n"] = 3
    an_action = add_two
    an_action(ctx)

    assert ctx["result"] == 5


def test_fn__will_not_execute_if_in_failed_state(ctx: Context) -> None:
    ctx.fail()
    ctx["n"] = 3
    add_two(ctx)

    assert "result" not in ctx.keys()


class TestActionExpects:
    def test_expects_keys_all_found(self, ctx: Context) -> None:
        @action(expects=["n", "y"])
        def action_dummy(ctx: Context) -> Context:
            pass

        ctx["n"] = 3
        ctx["y"] = 4
        action_dummy(ctx)

        assert ctx.is_success

    def test_expects_keys_misses_one(self, ctx: Context) -> None:
        @action(expects=["n", "y"])
        def action_dummy(ctx: Context) -> Context:
            pass

        ctx["n"] = 3

        with pytest.raises(ExpectedKeyNotFoundError) as exception:
            action_dummy(ctx)

        assert exception.value.args[0] == "Missing keys: ['y']"


class TestActionPromises:
    def test_promises_keys_all_found(self, ctx: Context) -> None:
        @action(expects=["n"], promises=["y"])
        def action_dummy(ctx: Context) -> Context:
            ctx["y"] = 4
            return ctx

        ctx["n"] = 3
        action_dummy(ctx)

        assert ctx.is_success

    def test_promises_keys_not_found(self, ctx: Context) -> None:
        @action(expects=["n"], promises=["y"])
        def action_dummy(ctx: Context) -> Context:
            pass

        ctx["n"] = 3
        with pytest.raises(PromisedKeyNotFoundError) as exception:
            action_dummy(ctx)

        assert exception.value.args[0] == "Promised keys not found: ['y']"
