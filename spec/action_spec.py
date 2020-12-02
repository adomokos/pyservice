from mamba import before, context, description, it  # type: ignore
from expects import expect, raise_error  # type: ignore
from pyservice.context import Context
from pyservice.action import action, Action  # , Action


@action()
def addTwo(ctx: Context) -> Context:
    n = ctx['n']
    ctx['result'] = n + 2
    return ctx


@action()
def addThree(ctx: Context) -> Context:
    n = ctx['n']
    ctx['result'] = n + 3
    return ctx


class AddTwo(Action):

    def execute(self, ctx):
        n = ctx['n']
        ctx['result'] = n + 2
        return ctx


with description('Action') as self:
    with before.each:
        self.ctx = Context.make()

    with context('wrapped action'):
        with it('can operate on a Context'):
            self.ctx['n'] = 3
            an_action = addTwo
            an_action(self.ctx)

            assert self.ctx['result'] == 5

        with it('will fail if the required key is not found'):
            self.ctx['x'] = 3

            expect(lambda: addTwo(self.ctx)).to(
                raise_error(KeyError))

        with it('will not execute if it is in failed state'):
            self.ctx.fail()
            self.ctx['n'] = 3
            addTwo(self.ctx)

            assert 'result' not in self.ctx.keys()

    with context('abstract class'):
        with it('can use an instance method'):
            self.ctx['n'] = 2
            a2 = AddTwo()
            a2.execute(self.ctx)
            assert self.ctx['result'] == 4

        with it('execution guarded by state of context'):
            self.ctx['n'] = 2
            self.ctx.fail()
            AddTwo().execute(self.ctx)

            assert 'result' not in self.ctx.keys()
