import functools
from pyservice.action import Action
from pyservice.context import Context
from itertools import takewhile
from typing import Callable, List


class Organizer2:
    def __init__(self, actions: List[Callable]):
        self.actions = actions

    def run(self, ctx: Context) -> Context:
        return functools.reduce(lambda _ctx, f: f(_ctx), self.actions, ctx)


class Organizer:
    class ContextFailed(Exception):
        def __init__(self, action: Action):
            self.action = action

    def __init__(self, ctx, actions):
        self.ctx = ctx
        self.actions = actions

    def run(self):
        return self._reduce(self.ctx, self.actions)

    def _reduce(self, ctx, actions):
        try:
            return functools.reduce(self._execute_action, actions, ctx)
        except Organizer.ContextFailed as e:
            # roll back the actions in reverse order
            actions_to_roll_back = self._find_actions_to_roll_back(e.action, actions)

            result = functools.reduce(self._execute_rollback, actions_to_roll_back, ctx)

            return ctx if result is None else result

    def _execute_action(self, ctx, action):
        result = action.execute(ctx)

        if result.is_failure:
            raise Organizer.ContextFailed(action)

        return result

    def _execute_rollback(self, ctx, action):
        return action.rollback(ctx)

    def _find_actions_to_roll_back(
        self, action: Action, actions: List[Action]
    ) -> List[Action]:

        actions_to_roll_back = [
            *takewhile(lambda a, x=action: a != x, actions)  # type: ignore
        ]
        actions_to_roll_back.reverse()
        return actions_to_roll_back
