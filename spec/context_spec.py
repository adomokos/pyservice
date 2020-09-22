from mamba import before, description, it  # type: ignore
from pyservice.context import Context


with description('Context') as self:
    with before.each:
        self.ctx = Context.make()

    with it('is success by default'):
        assert self.ctx.get_success()
        assert self.ctx.get_failure() is False

    with it('can be pushed into a failure state'):
        self.ctx.fail()
        assert self.ctx.get_failure()

    with it('is a dictionary'):
        self.ctx['one'] = 1
        assert self.ctx['one'] == 1
