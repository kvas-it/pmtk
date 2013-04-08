"""
PPL reader
"""

import shlex

from pmtk.model import project


class InvalidReaderInput(ValueError):
    """Invalid input to the reader."""


class PrematureEOF(InvalidReaderInput):
    """File ended where it should not have..."""


class UnexpectedCommand(InvalidReaderInput):
    """This command doesn't make sence here."""


class SyntaxError(InvalidReaderInput):
    """The reader can't understand the syntax"""


class Reader:
    """Read and pre-parse .ppl file(s)."""

    def __init__(self):
        self.stream = None
        self._reset()

    def _reset(self, filename=None):
        if filename is not None:
            self.filename = filename
        self.line_no = 0
        self.project = None
        self.context = None

    def _getNextLine(self):
        for line in self.stream:
            self.line_no += 1
            if line.isspace():
                continue
            if line.strip().startswith('--'):
                continue
            return line
        return None  # EOF

    def _splitLine(self, line):
        """Split line into tokens.

        Generally the line should be of the form:
        <indent><token> <token> ... [(<subcmd>, <subcmd>, ...)] [--<comment>]
        where:
          * indent is spaces or tabs which will only be counted,
          * tokens are sequences of alphanumeric characters or quoted strings,
          * subcmds are ...
          * comment is anything until the end of the string.

        The return values is a tuple (indent, token, token, (subcmd, subdmd)).
        """
        indent = 0
        while line[0].isspace():
            line = line[1:]
            indent += 1
        tokens = shlex.split(line)
        return (indent,) + tuple(tokens)

    def readFromStream(self, stream):
        """Read lines from the stream"""
        self.stream = stream
        self._reset()
        first_line = self._getNextLine()
        if first_line is None:
            raise PrematureEOF("Input file contains no commands")
        t = self._splitLine(first_line)
        if t[0] != 0:
            raise SyntaxError("Unexpected indent")
        if t[1] != 'Project':
            raise UnexpectedCommand("File must start with a Project command")
        if len(t) < 3:
            raise SyntaxError("Project must have an id")
        self.project = project.Project(t[2])  # id
        if len(t) > 3:
            self.project.title = t[3]  # title
        return self.project
