import inspect

is_job = lambda x: hasattr(x, '_hatter')


def get_jobs(module):
    """
    this method could only have been written in a sleep deprived stupor
    """
    jobs = {obj[1].dependency: obj[1] for obj in inspect.getmembers(module)
            if is_job(obj[1])}

    last = jobs.pop(-1)
    first = jobs.pop(False)

    reversed_tasks = []

    def cascade(job):
        if job.dependency is False:
            reversed_tasks.insert(0, job)

        if job not in reversed_tasks:
            reversed_tasks.append(job)
            cascade(job.dependency)

    for job in jobs.values():
        cascade(job)

    tasks = reversed_tasks[::-1]
    tasks.remove(first)
    tasks.insert(0, first)
    tasks.append(last)

    return tasks
