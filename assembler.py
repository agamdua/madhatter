import inspect

from collections import OrderedDict


is_job = lambda x: hasattr(x, '_parallel_mode')
parallel_mode = lambda x: x._parallel_mode


def get_jobs(module):
    tasks = sorted(
        [obj for obj in inspect.getmembers(module) if is_job(obj[1])],
        key=lambda x: parallel_mode(x[1])
    )
    return OrderedDict(tasks)
