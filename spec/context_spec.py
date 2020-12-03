from mamba import before, description, it  # type: ignore
from pyservice import Context


with description("Context") as self:
    with before.each:
        self.ctx = Context.make()

    with it("is success by default"):
        assert self.ctx.is_success
        assert self.ctx.is_failure is False

    with it("can be pushed into a failure state"):
        self.ctx.fail()
        assert self.ctx.is_failure

    with it("is a dictionary"):
        self.ctx["one"] = 1
        assert self.ctx["one"] == 1
