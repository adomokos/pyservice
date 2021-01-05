# `pyservice`

![build](https://github.com/adomokos/pyservice/workflows/Python%20Build/badge.svg)
[![PyPI version](https://badge.fury.io/py/pyservice.svg)](https://badge.fury.io/py/pyservice)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](http://opensource.org/licenses/MIT)

A [light-service](https://github.com/adomokos/light-service) influenced project in Python.

## Intro

Are you tired of 500 lines long Python code with conditionals, iterators, and function calls? Testing this logic is close to impossible, and with the lack of testing, you don't dare to touch it.

All complex logic can be decomposed into small functions, invoked sequentially. The functions should protect themselves from execution if a previous failure occurs, a more elegant solution exists: [Railway-Oriented Programming](https://fsharpforfunandprofit.com/rop/).

Let's see how that looks with `pyservice`. There are two functions, one that adds 2 to the initial number, and one that adds 3. The data is carried over between the functions in an extended dictionary we call [Context](pyservice/context.py), just like how a conveyor belt would be used in an assembly line:

```python
from pyservice import action, Context, Organizer


@action()
def add_two(ctx: Context) -> Context:
    number = ctx.get("n", 0)

    ctx["result"] = number + 2

    return ctx


@action()
def add_three(ctx: Context) -> Context:
    result = ctx["result"]

    ctx["result"] = result + 3

    return ctx


def test_can_run_functions():
    ctx = Context.make({"n": 4})
    organizer = Organizer([add_two, add_three])
    result_ctx = organizer.run(ctx)

    assert ctx.is_success
    assert result_ctx["result"] == 9
```

The `Context` is an extended dictionary, it stores failure and success state in it besides its key-value pairs. This is the "state" that is carried between the actions by the [Organizer](pyservice/organizer.py). All Organizers expose a `run` function which is responsible for executing the provided actions in order.

This is the happy path, but what happens when there is a failure between the two functions? I add a `fail_context` function that will fail the context with a message:

```python
@action()
def fail_context(ctx: Context) -> Context:
    ctx.fail("I don't like what I see here")
    return ctx
```

The context will be in a failure state and only the first action will be executed as processing stops after the second action (4+2=6):

```python
def test_can_run_functions_with_failure():
    ctx = Context.make({"n": 4})
    organizer = Organizer([add_two, fail_context, add_three])
    result_ctx = organizer.run(ctx)

    assert ctx.is_failure
    assert result_ctx["result"] == 6
```

Look at the actions, no conditional logic was added to them, the function wrapper protects the action from execution once it's in a failure state.

You can find these examples [here](test/test_example_1.py).

But there is more to it!


## Expects and Promises

You can define contracts for the actions with the `expects` and `promises` list of keys like this:


