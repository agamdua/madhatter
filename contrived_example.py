"""
The programmer will be encouraged to think in a 3 step process:
  - preprocessing (before)
  - parallel step(s): if multiple they will define the order
  - postprocessing (after)
"""

from decorators import depends, parallel, preprocess, postprocess


@preprocess
def hello():
    """
    Return a sequence which can be consumed by the next job
    """
    return [1, 2, 3, 4]


@depends(hello)
@parallel(n=4)
def job(sequence):
    """
    This could be any sequence that we can break up into
    multiple independent parts

    This could be generated from the `before` job, or
    from somewhere else entirely.
    """
    return tuple(sequence)


@depends(job)
@parallel(n=2)
def another_job(sequence_from_job):
    """
    This has to be unrelated to "job", and the order needs
    to explicitly be set if there is more than one parallel
    job.
    """
    return tuple(sequence_from_job)


@postprocess
def result(job_output):
    return list(job_output)
