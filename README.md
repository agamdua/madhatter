Madhatter
=========
[![Build
Status](https://travis-ci.org/agamdua/madhatter.svg)](https://travis-ci.org/agamdua/madhatter)
[![Coverage
Status](https://coveralls.io/repos/agamdua/madhatter/badge.svg?branch=master&service=github)](https://coveralls.io/github/agamdua/madhatter?branch=master)

Experimental data processing pipeline with job parallelization on those time-consuming for
loops.

Problem statement
=================
Python does not "magically" handle parallel execution, one has to muck about with `multiprocessing` and/or other libraries need to be leveraged and that can be a chore, especially if what one needs is really a cluster and not differnet processes on the same machine.


Objective
=========

`madhatter` attempts to take the work out of a data processing problem (wild unicorn appears!) so that the programmer can focus on the task at hand. 

The aim is to have minimal dependencies in the actual implementation, and to leverage the standard lib as much as possible.

The programmer should be able to construct their data execution chain where simple python functions (with a `madhatter` decorator) will serve as each `filter` in the chain (see below, design section for details).

This will also attempt to integrate with containers (docker to start with) so that each task may have the ability to be spun off into its own execution environment from a where a naive scheduler from `madhatter` can be used to pass this off to the host OS scheduling.

There is a web interface planned which will integrate with a message queue for async operations. That interface will most likely have `madhatter` as a dependency.


Architecture & Design
=====================
This follows the [pipes and filters](http://www.cs.olemiss.edu/~hcc/csci581oo/notes/pipes.html) design pattern.

There's a [great article on MSDN ](https://msdn.microsoft.com/en-us/library/dn568100.aspx) about such a pipeline where they describe the model pretty well:

> Decompose the processing required for each stream into a set of discrete components (or filters), each of which performs a single task. By standardizing the format of the data that each component receives and emits, these filters can be combined together into a pipeline.

Future Direction
================

Please refer [this
conversation](https://github.com/agamdua/madhatter/commit/0ca334a745d9833785ae33d62e61975d41527f38#commitcomment-14549012) on the first commit for the design plans.

Thanks, @miki725 for forcing me to write them out.


Examples
========

Please check out the `contrived_examples` module in the repo.
