from mamba import before, description, it  # type: ignore
from expects import expect, raise_error  # type: ignore
from pyservice.context import Context
from pyservice.action import action


@action()
def addTwo(ctx: Context) -> Context:
    n = ctx['n']
    ctx['result'] = n + 2
    return ctx


with description('Action') as self:
    with before.each:
        self.ctx = Context.make()

    with it('can operate on a Context'):
        self.ctx['n'] = 3
        addTwo(self.ctx)

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
