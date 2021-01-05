import functools
from pyservice.action import Action
from pyservice.context import Context
from itertools import takewhile
from typing import List


class Organizer:
    class ContextFailed(Exception):
        def __init__(self, action: Action):
            self.action = action

    def __init__(self, actions: List[Action]):
        self.actions = actions

    def run(self, ctx: Context) -> Context:
        try:
            return functools.reduce(lambda _ctx, f: f(_ctx), self.actions, ctx)
        except Organizer.ContextFailed as e:
            # roll back the actions in reverse order
            actions_to_roll_back = self._find_actions_to_roll_back(
                e.action, self.actions
            )

            result = functools.reduce(self._execute_rollback, actions_to_roll_back, ctx)

            return ctx if result is None else result

    @staticmethod
    def _execute_rollback(ctx: Context, action: Action):
        return action(ctx)

    @staticmethod
    def _find_actions_to_roll_back(
        action: Action, actions: List[Action]
    ) -> List[Action]:

        actions_to_roll_back = [
            *takewhile(lambda a, x=action: a != x, actions)  # type: ignore
        ]
        actions_to_roll_back.reverse()
        return actions_to_roll_back
