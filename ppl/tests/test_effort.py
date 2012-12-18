"""
$Id$

Tests for the effort estimates
"""

import unittest
import setup

from ppl.project import Project


class EffortTest(unittest.TestCase):

    def test_simple_task(self):
        p = Project()
        p.addTask('a')
        p.addTask('b')
        p.addEstimate('a', 5)
        self.failUnlessEqual(p.getTotalEffort(), 5)
        p.addTask('ba', parent='b')
        p.addTask('bb', parent='b')
        p.addEstimate('ba', 3)
        p.addEstimate('bb', 2)
        self.failUnlessEqual(p.getTotalEffort(), 10)


if __name__ == '__main__':
    unittest.main()

