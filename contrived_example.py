"""
The programmer will be encouraged to think in a 3 step process:
  - preprocessing (before)
  - parallel step(s): if multiple they will define the order
  - postprocessing (after)
"""

from madhatter import before, parallel, after


@before
def hello():
    print("Hey!")


@parallel(number=4, order=1)  # "number": number of splits to run in parallel
def job(sequence):
    """
    This could be any sequence that we can break up into
    multiple independent parts

    This could be generated from the `before` job, or
    from somewhere else entirely.
    """
    print(list(sequence))


@parallel(number=2, order=2)
def another_job(another_or_even_same_sequence):
    """
    This has to be unrelated to "job", and the order needs
    to explicitly be set if there is more than one parallel
    job.
    """
    print(list(another_or_even_same_sequence))


@after
def result(job_output):
    print("result!")
