from mamba import before, description, it  # type: ignore
from pyservice import Context


with description("Context") as self:
    with before.each:
        self.ctx = Context.make()

    with it("is success by default"):
        assert self.ctx.is_success
        assert self.ctx.is_failure is False

    with it("is not skipped by default"):
        assert self.ctx.is_skipped is False

    with it("can be pushed into a failure state"):
        self.ctx.fail()
        assert self.ctx.is_failure

    with it("can be pushed into a skipped state"):
        self.ctx.skip("No need to run the rest")
        assert self.ctx.is_skipped
        assert self.ctx.message == "No need to run the rest"

    with it("can fail with a message"):
        self.ctx.fail("An error occurred")
        assert self.ctx.is_failure
        assert self.ctx.message == "An error occurred"

    with it("is a dictionary"):
        self.ctx["one"] = 1
        assert self.ctx["one"] == 1
