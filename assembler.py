import inspect

from collections import OrderedDict


is_job = lambda x: hasattr(x, '_parallel_mode')
parallel_mode = lambda x: x._parallel_mode


def get_tasks(module):
    tasks = sorted(
        [obj for obj in inspect.getmembers(module) if is_job(obj[1])],
        key=lambda x: parallel_mode(x[1])
    )
    return OrderedDict(tasks)


class Assembly(object):
    get_tasks = get_tasks

    def __init__(self, module, *args, **kwargs):
        self.module = module

    def get_arguments_for_func(function_name):
        """
        Returns a tuple, dict pair.

        This has to be implemented depending on what context this is running
        in.

        For example, the user may enter these on a form on the web UI.
        """
        pass

    def assemble(self):
        tasks = self.get_tasks(self.module)
        for task in tasks:
            arguments = self.get_arguments_for_func(task)
            func = tasks[task]
            tasks[task] = {'func': func, 'arguments': arguments}
        return tasks

    def executees(self):
        """
        Returns an OrderedDicts where the key is the function name,
        and value is a dict which contains the callable and arguments it is to
        receive

        One method feeds into the other, chaining I guess.

        At the moment we can make the assumption that there is only one
        ``before`` and one ``after``. everything else in the middle can be run
        as parallel jobs on their ``sequence`` argument.

        The thought is that the pre- and post- processing steps should not be
        as time consuming, and the the actual processing step would be the one
        we can split up.
        """
        return self.assemble()

    def _task_map(self, task):
        return self.executees[task]

    def _get_func(self, task):
        self._task_map(task)['func']

    def _get_args(self, task):
        self._task_map(task)['arguments']

    def get_parallel_mode(self, task):
        return self._task_map(task).get('_parallel_mode')

    def execute_function(self, task):
        func = self._get_func(task)
        arguments = self._get_args(task)
        return func(*arguments[0], **arguments[1])

    def parallel(self, task, previous, **kwargs):
        """
        Need to override for parallel behavior.

        In the absence of a parallel backend we will actually just execute
        in sequence.
        """
        # TODO: log that we are not being able to execute in parallel
        # TODO: need a hook for previos sequence to be added
        return self.execute_function(task)

    def execute_pipeline(self):
        before = None
        parallel = []
        after = None

        for task in self.executees:
            parallel_mode = self.get_parallel_mode(task)
            if parallel_mode == 1:
                before = self.execute_function(task)
                # the before step should always return an iterable
                continue

            if parallel_mode == 2:
                if parallel:
                    raise NotImplementedError(
                        "At this point we assume only one parallel job"
                    )
                parallel.append(self.parallel(self._task_map(task), before))
                continue

            if parallel_mode == 3:
                last_parallel_result = parallel[-1]
                # TODO: need to add hook for last_parallel_result to be added
                # as an argument to the task, same as above.
                after = self.execute_function(task)

        return after
