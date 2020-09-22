from mamba import before, description, it  # type: ignore
from pyservice.context import Context
from pyservice.action import action
from typing import Callable, List


@action()
def addTwo(ctx: Context) -> Context:
    n = ctx['n']
    ctx['result'] = n + 2
    return ctx


@action()
def addThree(ctx: Context) -> Context:
    ctx['result'] += 3
    return ctx


def organizer(ctx: Context) -> Context:
    actions: List[Callable] = [addTwo, addThree]
    for an_action in actions:
        an_action(ctx)

    return ctx


with description('Organizer') as self:
    with before.each:
        self.ctx = Context.make()

    with it('can operate on Actions'):
        self.ctx['n'] = 3
        organizer(self.ctx)

        assert self.ctx['result'] == 8
