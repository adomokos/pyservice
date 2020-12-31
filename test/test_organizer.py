import pytest
from pyservice import action, Context, Organizer, Organizer2
from typing import Callable, List
from .test_doubles import AddTwo, AddTwoWithRollback, AddThree, Fail


@action()
def add_two(ctx: Context) -> Context:
    n = ctx["n"]

    result = ctx.get("result", n)

    ctx.update(result=result + 2)
    return ctx


@action()
def fail_context(ctx: Context) -> Context:
    ctx.fail("Something went wrong...")
    return ctx


@action()
def skip_rest(ctx: Context) -> Context:
    ctx.skip("No need to run the rest")
    return ctx


@action()
def add_three(ctx: Context) -> Context:
    ctx["result"] += 3
    return ctx


def organizer(ctx: Context) -> Context:
    actions: List[Callable] = [add_two, add_three]
    for an_action in actions:
        an_action(ctx)

    return ctx


def organizer2(ctx: Context) -> Context:
    ctx["result"] = 2
    actions = [AddTwo, AddThree]
    for an_action in actions:
        an_action().execute(ctx)

    return ctx


@pytest.fixture
def ctx() -> Context:
    return Context.make()


# Using functions
def test_can_operate_on_action_functions(ctx: Context) -> None:
    ctx["n"] = 3
    organizer(ctx)

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


# Using Action objects
def test_can_call_two_actions(ctx: Context) -> None:
    ctx["result"] = 2
    o2 = Organizer(ctx, [AddTwo(), AddThree()])

    o2.run()

    assert ctx["result"] == 7


def test_will_stop_executing_after_failed_action(ctx: Context) -> None:
    ctx["result"] = 2
    o3 = Organizer(ctx, [AddTwo(), Fail(), AddThree()])

    result3: Context = o3.run()

    assert result3.is_failure
    assert result3["result"] == 4


def test_rolls_back_with_available_rollbacks(ctx: Context) -> None:
    ctx["result"] = 2
    o4 = Organizer(ctx, [AddTwoWithRollback(), Fail(), AddThree()])

    result4: Context = o4.run()
    assert result4.is_failure
    assert result4["result"] == 2
