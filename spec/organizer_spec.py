from mamba import before, context, description, it  # type: ignore
from pyservice.context import Context
from pyservice.action import action
from pyservice.organizer import Organizer
from typing import Callable, List
from .test_doubles import AddTwo, AddThree


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


def organizer2(ctx: Context) -> Context:
    ctx['result'] = 2
    actions = [AddTwo, AddThree]
    for an_action in actions:
        an_action().execute(ctx)

    return ctx


with description('Organizer') as self:
    with before.each:
        self.ctx = Context.make()

    with context('using functions'):

        with it('can operate on action functions'):
            self.ctx['n'] = 3
            organizer(self.ctx)

            assert self.ctx['result'] == 8

    with context('using Action objects'):

        with it('can call two actions'):
            self.ctx['result'] = 2
            o2 = Organizer(self.ctx, [AddTwo(), AddThree()])

            o2.run()

            assert self.ctx['result'] == 7
