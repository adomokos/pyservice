from typing import Callable, List

from pyservice import action
from pyservice import Action
from pyservice import Context


@action(expects=["n"])
def add_two(ctx: Context) -> Context:
    n = ctx["n"]

    result = ctx.get("result", n)

    ctx.update(result=result + 2)
    return ctx


@action(promises=["result"])
def add_three(ctx: Context) -> Context:
    ctx["result"] += 3
    return ctx


@action()
def fail_context(ctx: Context) -> Context:
    ctx.fail("Something went wrong...")
    return ctx


@action()
def skip_rest(ctx: Context) -> Context:
    ctx.skip("No need to run the rest")
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


class AddTwo(Action):
    def execute(self, ctx: Context) -> Context:
        ctx["result"] += 2
        return ctx


class AddTwoWithRollback(Action):
    def execute(self, ctx: Context) -> Context:
        ctx["result"] += 2
        return ctx

    def rollback(self, ctx: Context) -> Context:
        ctx["result"] -= 2
        return ctx


class AddThree(Action):
    def execute(self, ctx: Context) -> Context:
        ctx["result"] += 3
        return ctx


class Fail(Action):
    def execute(self, ctx: Context) -> Context:
        ctx.fail()
        return ctx
