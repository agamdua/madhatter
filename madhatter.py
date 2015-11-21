"""
Decorators that will allow an importer to identify the different steps
of execution.

These could be:
  - preprocessing (before)
  - parallel
  - postprocessing (after)

Below is the infrastructure and a couple of functions that are more
exemplary than useful.

TODO:
    - check that they are not executing the function calls in the file (regex)
"""


def apply_props(func, name, step_number, number=None, order=None):
    func.__name__ = name
    func._parallel_mode = step_number
    func.cores = number
    func.substep_number = order
    return func


def decorator(name, step):
    """
    Returns a decorator that of a user-provided name,
    and a step_order which corresponds to when in the
    data pipeline it should execute.

    Args:
        name (str): name of the decorator required
        step_order (int): what step the function should execute at
            in the data pipeline.
    """
    def step_with_arguments(ofunc=None, number=None, order=None):
        def execution_step(func):
            def func_wrapper(*args, **kwargs):
                func(*args, **kwargs)
            return apply_props(func_wrapper, name, step, number, order)

        apply_props(execution_step, name, step, number, order)

        if ofunc:
            return execution_step(ofunc)

        return execution_step
    return step_with_arguments

before = decorator('before', 1)
parallel = decorator('parallel', 2)
after = decorator('after', 3)
