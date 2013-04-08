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
        wb = """
-- This is a comment and it will be ignored
Project 3322 "Empty project test"
"""
        prj = self._read_string(wb)
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
            self._read_string('Other Command')
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

#     def test_work_breakdown(self):
#         """Test reading of a simple work breakdown structure"""
#         wb = """
# 




if __name__ == '__main__':
    unittest.main()

