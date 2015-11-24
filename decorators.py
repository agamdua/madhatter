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

from functools import partial, wraps


def depends(*args):
    """
    Specify the step that needs to execute before the current step

    This will usually be the function that is envisioned to
    execute right before this step is performed.

    This is required to execute the chain in the correct order.

    At the moment these is support for only one dependency.
    """
    def wrapper(func):
        func.dependency = args[0]
        func._hatter = True
        return func
    return wrapper


def preprocess(func):
    func.dependency = False
    func._hatter = True
    return func


def postprocess(func):
    func._hatter = -1
    func.end = True
    return func


def parallel(ofunc=None, n=None, chunk_by=None):
    def apply_props(func, n, chunk_by):
        func.n = n
        func.chunk_by = chunk_by
        return func

    decorate = partial(apply_props, n=n, chunk_by=chunk_by)

    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            return func(*args, **kwargs)
        return decorate(wrapped)

    if ofunc is not None:
        return decorate(wrapper(ofunc))

    return decorate(wrapper)
