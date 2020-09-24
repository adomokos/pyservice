import functools


class Organizer():

    def __init__(self, ctx, actions):
        self.ctx = ctx
        self.actions = actions

    def run(self):
        return self._reduce(self.ctx, self.actions)

    def _reduce(self, ctx, actions):
        return functools.reduce(self._execute_action, actions, ctx)

    def _execute_action(self, ctx, action):
        action.execute(ctx)
        return ctx
