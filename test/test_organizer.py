import pytest
from pyservice import Context, Organizer2
from .test_doubles import (
    add_two,
    add_two_with_rollback,
    add_three,
    add_three_with_rollback,
    organizer,
    fail_context,
    skip_rest,
)


@pytest.fixture
def ctx() -> Context:
    return Context.make()


# Using functions
def test_can_operate_on_action_functions(ctx: Context) -> None:
    ctx["n"] = 3
    organizer.run(ctx)

    assert ctx["result"] == 8


def test_can_run_functions(ctx: Context) -> None:
    ctx["n"] = 3
    actions = Organizer2([add_two, add_three])

    result_ctx = actions.run(ctx)

    assert result_ctx["result"] == 8


def test_can_stop_with_failure(ctx: Context) -> None:
    ctx["n"] = 3
    actions_with_failure = Organizer2([add_two, fail_context, add_three])

    result_ctx = actions_with_failure.run(ctx)

    assert result_ctx["result"] == 5
    assert result_ctx.is_failure


def test_skip_the_rest_of_the_actions(ctx: Context) -> None:
    ctx["n"] = 3
    actions_with_skip = Organizer2([add_two, skip_rest, add_three])

    result_ctx = actions_with_skip.run(ctx)

    assert result_ctx["result"] == 5, result_ctx
    assert result_ctx.is_success
    assert result_ctx.is_skipped


def test_can_call_nested_organizer_actions(ctx: Context) -> None:
    ctx["n"] = 3

    nestable_organizer = Organizer2([add_two, add_three])
    nested_organizer = Organizer2([add_two, add_three, nestable_organizer.run])

    # Run function under test
    result_ctx = nested_organizer.run(ctx)

    assert result_ctx.is_success
    assert result_ctx["result"] == 13


def test_can_fail_nested_organizers_action(ctx: Context) -> None:
    ctx["n"] = 3

    nestable_organizer = Organizer2([add_two, fail_context, add_three])
    nested_organizer = Organizer2([add_two, add_three, nestable_organizer.run])

    # Run function under test
    result_ctx = nested_organizer.run(ctx)

    assert result_ctx.is_failure
    # Stops at the 3rd action: adds 2, 3 and 2 to initial 3 => 10
    assert result_ctx["result"] == 10


def test_rolls_back_action_when_rollback_found(ctx: Context) -> None:
    ctx["n"] = 3

    rollback_organizer = Organizer2(
        [add_two_with_rollback, add_three_with_rollback, fail_context]
    )

    # Run function under test
    result_ctx = rollback_organizer.run(ctx)

    assert result_ctx.is_failure
    assert result_ctx["result"] == 3
