from pyservice import Action
from pyservice import Context


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
