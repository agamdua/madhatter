import unittest

import contrived_example as module

from assembler import get_tasks as get_jobs
from contrived_example import hello, job, another_job, result


class MadhatterTest(unittest.TestCase):
    def test_property_setting(self):
        for task in [hello, job, another_job, result]:
            assert hasattr(task, '_parallel_mode')
            assert hasattr(task, 'cores')
            assert hasattr(task, 'substep_number')

    def test_get_jobs(self):
        jobs = get_jobs(module)
        assert len(jobs) == 4


if __name__ == '__main__':
    unittest.main()
