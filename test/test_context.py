import pytest
from pyservice import Context


@pytest.fixture
def ctx() -> Context:
    return Context.make()


def test_is_success_by_default(ctx: Context) -> None:
    assert ctx.is_success
    assert ctx.is_failure is False


def test_is_not_skipped_by_default(ctx: Context) -> None:
    assert ctx.is_skipped is False


def test_can_be_pushed_into_a_failure_state(ctx: Context) -> None:
    ctx.fail()
    assert ctx.is_failure


def test_can_be_pushed_into_a_skipped_state(ctx: Context) -> None:
    ctx.skip("No need to run the rest")
    assert ctx.is_skipped
    assert ctx.message == "No need to run the rest"


def test_can_fail_with_a_message(ctx: Context) -> None:
    ctx.fail("An error occurred")
    assert ctx.is_failure
    assert ctx.message == "An error occurred"


def test_is_a_dictionary(ctx: Context) -> None:
    ctx["one"] = 1
    assert ctx["one"] == 1
