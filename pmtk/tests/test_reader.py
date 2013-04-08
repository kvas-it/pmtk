"""
Tests for the ppl reader
"""

import unittest
import base

from pmtk.ppl import reader
import StringIO


class TestReader(unittest.TestCase):
    """Tests for the Reader class."""

    def _read_string(self, s):
        sio = StringIO.StringIO(s)
        rdr = reader.Reader()
        return rdr.readFromStream(sio)

    def test_empty_file(self):
        """Test reading an empty file -- should fail."""
        try:
            self._read_string('')
            raise AssertionError('PrematureEOF exception expected')
        except reader.PrematureEOF:
            pass

    def test_empty_project(self):
        """Test reading an empty project."""
        prj = self._read_string("""
-- This is a comment and it will be ignored
Project 3322 "Empty project test"
""")
        self.failUnlessEqual(prj.id, '3322')
        self.failUnlessEqual(prj.title, 'Empty project test')

    def test_empty_project_no_title(self):
        """Test reading an empty project with no title."""
        wb = """Project 3322"""
        prj = self._read_string(wb)
        self.failUnlessEqual(prj.id, '3322')
        self.failUnlessEqual(prj.title, '3322')

    def test_premature_commands(self):
        """Test handling of commands before Project"""
        try:
            self._read_string('Task a')
            raise AssertionError('UnexpectedCommand exception expected')
        except reader.UnexpectedCommand:
            pass

    def test_first_line_indent(self):
        """Indent first line and check that we fail"""
        try:
            self._read_string(' Project indented')
            raise AssertionError('SyntaxError expected')
        except reader.SyntaxError:
            pass

    def test_project_no_id(self):
        """Try to create a project with no id"""
        try:
            self._read_string('Project  -- without the id')
            raise AssertionError('SyntaxError expected')
        except reader.SyntaxError:
            pass

    def test_one_task(self):
        """Test one task project"""
        prj = self._read_string("""
Project 3322
Task a b
""")
        self.assertEqual(len(prj.getRootTask().listChildren()), 1)
        a = prj.getTask('.a')
        self.assertEqual(a.id, 'a')
        self.assertEqual(a.title, 'b')


    def test_task_and_subtask(self):
        """Test a project with a task and subtask"""
        prj = self._read_string("""
Project 3322
Task a
    Task b
""")
        a = prj.getTask('.a')
        self.assertEqual(len(a.listChildren()), 1) 
        b = a.navigate('b')
        self.assertEqual(b.id, 'b')
        self.assertEqual(b.title, 'b')


if __name__ == '__main__':
    unittest.main()

