"""
$Id$

Tests for the effort estimates
"""

import unittest
import setup

from ppl.project import Project


class EffortTest(unittest.TestCase):

    def test_simple_tasks(self):
        p = Project()
        p.addTask('a')
        p.addTask('b')
        p.addEstimate('a', 5)
        self.failUnlessEqual(p.getTotalEffort(), 5)


if __name__ == '__main__':
    unittest.main()

