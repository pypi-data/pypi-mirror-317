"""DALPy is a Python package for learning data structures and algorithms. It is based off of *Introduction to Algorithms*
by Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. This library was made specifically for
administering and grading assignments related to data structures and algorithms in computer science.

With this library students can receive progress reports on their problem sets in real time as they complete assignments.
Additionally, student submission assessment is done with unit tests, instead of hand-tracing, ensuring that the grades
that students receive accurately reflect their submissions.

The DALPy testing suite offers extremely lightweight and flexible unit testing utilities that can be used on any
kind of assignment, whether to write functions or build classes. Course administration can be easily streamlined by
restricting which library data structures students are allowed to use on any particular assignment.

DALPy began as a project by two Brandeis University undergraduate students to replace hand-written problem sets
written in pseudocode.

## Provided Data Structures
The DALPy library offers a set of fundamental data structures and algorithms, with behavior as specified by H.
Cormen et al.'s *Introduction to Algorithms*. The following structures (separated by module) are supported:

* [arrays](https://dalpy-developers.github.io/DALPy/arrays.html)
    * Array
    * Array2D
* [queues](https://dalpy-developers.github.io/DALPy/queues.html)
    * Queue
* [stacks](https://dalpy-developers.github.io/DALPy/stacks.html)
    * Stack
* [sets](https://dalpy-developers.github.io/DALPy/sets.html)
    * Set
* [linked_lists](https://dalpy-developers.github.io/DALPy/linked_lists.html)
    * SinglyLinkedListNode
    * DoublyLinkedListNode
* [trees](https://dalpy-developers.github.io/DALPy/trees.html)
    * BinaryTreeNode
    * NaryTreeNode
    * depth(NaryTreeNode)
* [hashing](https://dalpy-developers.github.io/DALPy/hashing.html)
    * HashTable
* [heaps](https://dalpy-developers.github.io/DALPy/heaps.html)
    * PriorityQueue
    * build_min_heap(Array)
* [graphs](https://dalpy-developers.github.io/DALPy/graphs.html)
    * Vertex
    * Graph

## Unit Testing
Along with the DALPy data structures come test utilities for writing test cases. The testing framework allows a
course administrator to easily write test cases for either expected function output or general class behavior. Test
cases can then be compiled into a testing suite. The testing suite has the capability to set a test case run-time 
timeout and to record comma-separated test results for administrative use.

Consider the example test case below:

    import unittest
    from dalpy.factory_utils import make_stack
    from dalpy.test_utils import build_and_run_watched_suite, generic_test

    from student_submission import student_function

    # TestCase class for testing student_function
    class StudentFunctionTest(unittest.TestCase):

        # A single test case
        def simple_test_case(self):
            stack = make_stack([1, 2, 3])
            expected = make_stack([1, 1, 2, 2, 3, 3])
            generic_test(stack, expected, student_function, in_place=True)

    # Run the test cases using build_and_run_watched_suite with a timeout of 4 seconds
    if __name__ == '__main__':
        build_and_run_watched_suite([StudentFunctionTest], 4)


## Installation

DALPy is [available on PyPI](https://pypi.org/project/dalpy/), and can be installed with pip.

    pip install dalpy

DALPy has the following dependencies:

    Python >= 3.6

## Issues

We encourage you to report issues using the GitHub tracker. We welcome all kinds of issues, especially those related to
correctness, documentation and feature requests.

## Academic Usage

If you are planning to use DALPy for a university course and have questions, feel free to reach out by email.

## Documentation

The full documentation for DALPy is available [here](https://dalpy-developers.github.io/DALPy/).

## Sample Usage

To view sample assignments using DALPy browse the [DALPy sample problems repository](https://github.com/DALPy-Developers/DALPy-Sample-Problems) on GitHub.

## Notes

This project was formerly known as Cormen-Lib.
"""