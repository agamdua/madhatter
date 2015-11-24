import unittest

import contrived_example as module

from assembler import get_jobs
from decorators import depends, parallel, preprocess, postprocess


class MadhatterTest(unittest.TestCase):
    def test_postprocess(self):
        @postprocess
        def job(sequence):
            pass

        assert job._hatter
        assert job([1, 2]) is None

    def test_preprocess(self):
        @preprocess
        def job(sequence):
            pass

        assert job([1, 2]) is None
        assert job._hatter

    def test_get_jobs(self):
        jobs = get_jobs(module)

        self.assertEqual(len(jobs), 4)
        self.assertEqual(jobs[0](), [1, 2, 3, 4])
        self.assertEqual(jobs[1].__name__, "job")
        self.assertEqual(jobs[1](jobs[0]()), (1, 2, 3, 4))

    def test_depends(self):
        fake_dependency = lambda x: x

        @depends(fake_dependency)
        def dependent_job(sequence):
            pass

        assert dependent_job.dependency == fake_dependency
        assert dependent_job._hatter

        assert dependent_job([1, 2, 3, 4]) is None

    def test_parallel_no_args(self):

        @parallel
        def parallel_job(sequence):
            pass

        assert parallel_job.n is None
        assert parallel_job.chunk_by is None
        assert parallel_job([1, 2]) is None

    def test_parallel_with_args(self):

        @parallel(n=4, chunk_by=1000)
        def parallel_job(sequence):
            pass

        assert parallel_job.n is 4
        assert parallel_job.chunk_by is 1000
        assert parallel_job([1, 2]) is None

if __name__ == '__main__':
    unittest.main()
