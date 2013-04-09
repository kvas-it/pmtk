"""
PPL reader
"""

import shlex
import itertools

from pmtk.model import project, work


class InvalidReaderInput(ValueError):
    """Invalid input to the reader."""


class PrematureEOF(InvalidReaderInput):
    """File ended where it should not have..."""


class UnexpectedCommand(InvalidReaderInput):
    """This command doesn't make sence here."""


class UnrecognizedCommand(InvalidReaderInput):
    """The command is not supported."""


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
        self.project = None
        self.line_no = 0
        self.indent_level = 0
        self.indent_level_stack = []
        self.context = None
        self.context_stack = []

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
        tokens = list(itertools.takewhile(lambda t: not t.startswith('--'),
            shlex.split(line)))  # split and drop the comment at the end
        return [indent] + tokens

    def _setContext(self, context, indent):
        """Set context and indent to the new values.

        Push old ones onto the stack."""
        if self.context is not None:
            self.context_stack.append(self.context)
            self.indent_level_stack.append(self.indent_level)
        self.context = context
        self.indent_level = indent

    def _popContext(self):
        """Pop last context and indent level from the stack."""
        assert len(self.context_stack) == len(self.indent_level_stack)
        if len(self.context_stack):
            self.context = self.context_stack.pop()
            self.indent_level = self.indent_level_stack.pop()
        else:
            self.context = None
            self.indent_level = 0

    def _handleIndent(self, indent):
        """Pop required number of contexts from the stack.

        If indent is greater than current, new node is under context, so we pop
        nothing. If it's the same as current, new node is a sibling of the
        context, so we pop one node. Otherwise pop until the indent of the
        context is less than the indent of the new node (means we got to its
        parent).
        """
        if indent > self.indent_level:
            if not self.context:
                raise SyntaxError("Unexpected indent")
        elif indent == self.indent_level:
            self._popContext()
        else:
            if indent not in self.indent_level_stack:
                raise SyntaxError("Unexpected unindent level")
            while self.indent_level >= indent:
                self._popContext()

    def _breakCommand(self, cmd_parts):
        """Break the command into command, arguments and extras."""
        if cmd_parts[0] in ('Project', 'Task'):
            cmd = cmd_parts.pop(0)
        else:
            if self.context is not None:
                cmd = self.context.command_name
            else:
                raise UnrecognizedCommand('Unknown command: %s' % cmd_parts[0])

        if self.project is None and cmd != 'Project':
            raise UnexpectedCommand("File must start with a Project command")

        return cmd, cmd_parts, []

    def _doOneCommand(self):
        """Read one command from the input file and execute it.

        Returns True if there was a command, False otherwise.
        """
        line = self._getNextLine()
        if line is None:
            return False

        t = self._splitLine(line)

        indent = t.pop(0)
        self._handleIndent(indent)

        cmd, args, extras = self._breakCommand(t)
        handler = getattr(self, '_handle%sCommand' % cmd)
        obj = handler(args, extras)

        self._setContext(obj, indent)

        return True

    def _handleProjectCommand(self, args, extras):
        if len(args) < 1:
            raise SyntaxError("Project must have an id")
        self.project = project.Project(args[0])  # id
        if len(args) > 1:
            self.project.title = args[1]  # title
        return self.project

    def _handleTaskCommand(self, args, extras):
        if len(args) < 1:
            raise SyntaxError("Task must have an id")
        elif len(args) == 1:
            id, title = args[0], None
        else:
            id, title = args[:2]

        if self.context is None:
            parent = self.project.getRootTask()
        else:
            parent = self.context

        return work.Task(id, title, parent)

    def readFromStream(self, stream):
        """Read lines from the stream"""
        self.stream = stream
        self._reset()

        if not self._doOneCommand():
            raise PrematureEOF("Input file contains no commands")

        while True:
            if not self._doOneCommand():
                break

        return self.project
