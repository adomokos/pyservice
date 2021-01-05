import functools
from pyservice.context import Context
from itertools import takewhile
from typing import Callable, List

Action2 = Callable[[Context], Context]


class Organizer2:
    class ContextFailed(Exception):
        def __init__(self, action: Action2):
            self.action = action

    def __init__(self, actions: List[Action2]):
        self.actions = actions

    def run(self, ctx: Context) -> Context:
        try:
            return functools.reduce(lambda _ctx, f: f(_ctx), self.actions, ctx)
        except Organizer2.ContextFailed as e:
            # roll back the actions in reverse order
            actions_to_roll_back = self._find_actions_to_roll_back(
                e.action, self.actions
            )

            result = functools.reduce(self._execute_rollback, actions_to_roll_back, ctx)

            return ctx if result is None else result

    def _execute_rollback(self, ctx: Context, action: Action2):
        return action(ctx)

    def _find_actions_to_roll_back(
        self, action: Action2, actions: List[Action2]
    ) -> List[Callable]:

        actions_to_roll_back = [
            *takewhile(lambda a, x=action: a != x, actions)  # type: ignore
        ]
        actions_to_roll_back.reverse()
        return actions_to_roll_back
