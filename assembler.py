import inspect

is_job = lambda x: hasattr(x, '_hatter')


def get_jobs(module):
    """
    this method could only have been written in a sleep deprived stupor
    """
    jobs = [obj[1] for obj in inspect.getmembers(module) if is_job(obj[1])]
    tasks = []

    last = [x for x in jobs if getattr(x, 'end', None)][0]

    def append_next(job):
        if job is False:
            return

        tasks.append(job)

        append_next(job.dependency)

    append_next(last)
    tasks.reverse()

    return tasks
