from mamba import before, context, description, it  # type: ignore
from pyservice import Context
from pyservice import action
from pyservice import Organizer, Organizer2
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


with description("Organizer") as self:
    with before.each:
        self.ctx = Context.make()

    with context("using functions"):

        with it("can operate on action functions"):
            self.ctx["n"] = 3
            organizer(self.ctx)

            assert self.ctx["result"] == 8

        with it("can run functions"):
            self.ctx["n"] = 3
            actions = Organizer2([add_two, add_three])

            result_ctx = actions.run(self.ctx)

            assert result_ctx["result"] == 8

        with it("can stop with failure"):
            self.ctx["n"] = 3
            actions_with_failure = Organizer2([add_two, fail_context, add_three])

            result_ctx = actions_with_failure.run(self.ctx)

            assert result_ctx["result"] == 5
            assert result_ctx.is_failure

        with it("can call nested organizer actions"):
            self.ctx["n"] = 3

            nestable_organizer = Organizer2([add_two, add_three])
            nested_organizer = Organizer2([add_two, add_three, nestable_organizer.run])

            # Run function under test
            result_ctx = nested_organizer.run(self.ctx)

            assert result_ctx.is_success
            assert result_ctx["result"] == 13

    with context("using Action objects"):

        with it("can call two actions"):
            self.ctx["result"] = 2
            o2 = Organizer(self.ctx, [AddTwo(), AddThree()])

            o2.run()

            assert self.ctx["result"] == 7

        with it("will stop executing after failed action"):
            self.ctx["result"] = 2
            o3 = Organizer(self.ctx, [AddTwo(), Fail(), AddThree()])

            result3: Context = o3.run()

            assert result3.is_failure
            assert result3["result"] == 4

        with it("rolls back with available rollbacks"):
            self.ctx["result"] = 2
            o4 = Organizer(self.ctx, [AddTwoWithRollback(), Fail(), AddThree()])

            result4: Context = o4.run()
            assert result4.is_failure
            assert result4["result"] == 2
