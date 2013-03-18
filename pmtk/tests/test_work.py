"""
Tests for the work breakdown module model.work.
"""

import unittest
import base

from pmtk.model.work import WorkBreakdownBuilder, WorkBreakdownMixin, Task,\
        ContextStackEmpty


class TestWB(WorkBreakdownMixin):
    pass


class TestWorkBreakdownMixin(unittest.TestCase):
    """Tests for WorkBreakdownMixin."""

    def test_sanity(self):
        """Basic sanity test of WorkBreakdownMixin methods."""
        wb = TestWB()
        root = wb.getRootTask()
        self.assertIs(root, wb.root_task)
        self.assertIs(wb.getTask('.'), root)
        task = Task('task', 'Task', root)
        subtask = Task('subtask', 'Subtask', task)
        self.assertIs(wb.getTask('.task'), task)
        self.assertIs(wb.getTask('.task.subtask'), subtask)
        self.assertIs(wb.getTask('subtask'), subtask)


class TestWorkBreakdownBuilder(unittest.TestCase):
    """Test the work breakdown structure bulding using WorkBreakdownBuilder."""

    def test_sanity(self):
        """use addTask in different ways."""
        wb = TestWB()
        wbb = WorkBreakdownBuilder(wb)
        wbb.setContext(wbb.addTask('a', '.a'))
        wbb.setContext(wbb.addTask('b', '.a.b'))
        wbb.addTask('c', '.a.b.c')
        wbb.addTask('d', '.a.b.d')
        wbb.popContext()
        wbb.addTask('e', '.a.e')
        wbb.popContext()
        wbb.addTask('e', '.e')
        self.assertRaises(ContextStackEmpty, wbb.popContext)
        wbb.navigateContext('c')
        wbb.addTask('e', '.a.b.c.e')
        wbb.addTask('d.f', '.a.b.d.f')
        wbb.addTask('a.d', '.a.d')
        for task in wb.getRootTask().yieldDescendants():
            self.assertEqual(task.title, task.getAbsolutePath())


if __name__ == '__main__':
    unittest.main()
