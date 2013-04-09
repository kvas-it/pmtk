"""
Tests for the ppl reader
"""

import unittest
import base  # noqa (base imported and not used, but it's ok)

from pmtk.ppl import reader
import StringIO


class TestReader(unittest.TestCase):
    """Tests for the Reader class."""

    def _read_string(self, s):
        """Read ppl file from string, return loaded project."""
        sio = StringIO.StringIO(s)
        rdr = reader.Reader()
        return rdr.readFromStream(sio)

    def test_empty_file(self):
        """Empty file -- should fail."""
        try:
            self._read_string('')
            raise AssertionError('PrematureEOF exception expected')
        except reader.PrematureEOF:
            pass

    def test_empty_project(self):
        """Reading an empty project."""
        prj = self._read_string("""
-- This is a comment and it will be ignored
Project 3322 "Empty project test"
""")
        self.failUnlessEqual(prj.id, '3322')
        self.failUnlessEqual(prj.title, 'Empty project test')

    def test_empty_project_no_title(self):
        """Reading an empty project with no title."""
        wb = """Project 3322"""
        prj = self._read_string(wb)
        self.failUnlessEqual(prj.id, '3322')
        self.failUnlessEqual(prj.title, '3322')

    def test_premature_commands(self):
        """Commands before Project -- must fail."""
        try:
            self._read_string('Task a')
            raise AssertionError('UnexpectedCommand exception expected')
        except reader.UnexpectedCommand:
            pass

    def test_first_line_indent(self):
        """Indent first line and check that we fail."""
        try:
            self._read_string(' Project indented')
            raise AssertionError('SyntaxError expected')
        except reader.SyntaxError:
            pass

    def test_project_no_id(self):
        """Try to create a project with no id -- must fail."""
        try:
            self._read_string('Project  -- without the id')
            raise AssertionError('SyntaxError expected')
        except reader.SyntaxError:
            pass

    def _read_tasks(self, task_str):
        """Read tasks description and return the list of tasks under root"""
        prj = self._read_string("""
Project 3372
""" + task_str)
        return prj.getRootTask().listChildren()

    def _read_task(self, task_str):
        """Read task(s) and return the first task under root."""
        return self._read_tasks(task_str)[0]

    def test_one_task(self):
        """One task project."""
        a = self._read_task("Task a b")
        root_task = a.getRoot()
        self.assertEqual(len(root_task.listChildren()), 1)
        a = root_task.navigate('.a')
        self.assertEqual(a.id, 'a')
        self.assertEqual(a.title, 'b')

    def test_task_no_id(self):
        """Task without id -- must fail."""
        try:
            self._read_task("Task")
            raise AssertionError('SyntaxError expected')
        except reader.SyntaxError:
            pass

    def test_task_hierarchy(self):
        """Project with a small task hierarchy."""
        a = self._read_task("""
Task a
    Task b
      Task c
""")
        self.assertEqual(len(a.listChildren()), 1)
        b = a.navigate('b')
        self.assertEqual(b.id, 'b')
        self.assertEqual(b.title, 'b')
        self.assertEqual(len(b.listChildren()), 1)
        c = b.navigate('c')
        self.assertEqual(c.id, 'c')
        self.assertEqual(c.title, 'c')

    def test_implicit_subtasks(self):
        """Omitting Task keyword for subtasks."""
        a, c = self._read_tasks("""
Task a
    b -- Task keyword can be omitted for subtasks
Task c
    d e
""")
        self.assertEqual(a.navigate('.a.b').title, 'b')
        self.assertEqual(c.navigate('.c.d').title, 'e')

    def test_task_hierarchy2(self):
        """Task hierarchy with some more branching."""
        tasks = self._read_tasks("""
Task a
    Task b
    Task c
Task d
    Task e
    Task f
""")
        self.assertEqual(len(tasks), 2)
        root_task = tasks[0].getRoot()
        a = root_task.navigate('.a')
        self.assertEqual(len(a.listChildren()), 2)
        d = root_task.navigate('.d')
        self.assertEqual(len(d.listChildren()), 2)

    def test_invalid_unindent(self):
        """Invalid unindent handling."""
        try:
            self._read_tasks("""
Task a
    Task b
  Task c
""")
            raise AssertionError('SyntaxError expected')
        except reader.SyntaxError:
            pass

    def test_task_description(self):
        """Task description loading."""
        a = self._read_task("""
Task a
    "First line of description"
    'Second line of description'
""")
        self.assertEqual(a.description, "First line of description\n"
                "Second line of description")

    def test_task_description_other_indent(self):
        """Task description with indent not matching the subtask indent.

        This is allowed and could be used to separate description from
        subtasks.
        """
        a = self._read_task("""
Task a
        "Description" -- this is description
    b subtask
""")
        self.assertEqual(a.description, "Description")
        self.assertEqual(a.navigate('.a.b').title, 'subtask')

    def test_mutiple_descriptions(self):
        """Project and task description loading."""
        prj = self._read_string("""
Project 3372 "Project 3372"
    "Description 3372"

Task a
    "Description a"
    ""
    "Third line"
    b
        "Description b"
Task c
    "Description c"
""")
        self.assertEqual(prj.description, 'Description 3372')
        self.assertEqual(prj.getTask('.a').description,
            'Description a\n\nThird line')
        self.assertEqual(prj.getTask('b').description, 'Description b')
        self.assertEqual(prj.getTask('c').description, 'Description c')


if __name__ == '__main__':
    unittest.main()
