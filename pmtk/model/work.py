"""
Classes related to work breakdown.
"""

from . import tree
from .. import util


class Task(tree.Node, util.TitleMixin):
    """Task is a basic element of work."""

    command_name = 'Task'  # for reader

    def __init__(self, id='', title=None, parent=None):
        tree.Node.__init__(self, id, parent)
        self.title = title


class WorkBreakdownMixin(object):
    """Container for the work breakdown (to be mixed into Project)."""

    def __init__(self):
        super(WorkBreakdownMixin, self).__init__()
        # root of the hierarchy of tasks
        self.root_task = Task()

    def getTask(self, path):
        """Look up task by absolute and relative path and return it."""
        return self.root_task.navigate(path)

    def getRootTask(self):
        """Return root task of the work breakdown structure."""
        return self.root_task


class ContextStackEmpty(Exception):
    """Raised by WorkBreakdownBuilder.popContext if context stack is empty."""


class WorkBreakdownBuilder(object):
    """Helper class for building work breakdown structure of the project.

    WBB keeps current context and a stack of previous contexts. It adds tasks
    under the current context.
    """

    def __init__(self, project):
        self.project = project
        self.context = project.getRootTask()
        self.context_stack = []  # previous contexts

    def setContext(self, new_context):
        """Set context to new_context and push current one onto the stack."""
        self.context_stack.append(self.context)
        self.context = new_context

    def navigateContext(self, path):
        """Navigate to a task by path and make it new context."""
        self.setContext(self.context.navigate(path))

    def popContext(self):
        """Replace current context with the last one from the stack."""
        if self.context_stack:
            self.context = self.context_stack.pop()
        else:
            raise ContextStackEmpty()

    def addTask(self, path, title):
        """Add a new task, and return it.

        Path can be just an id (then the task is created under current context)
        or a path (then prefix is navigated from the current context and then
        the last part of the path is used as the id of the new task).
        """
        if '.' in path:
            parent_path, new_id = path.rsplit('.', 1)
            parent = self.context.navigate(parent_path)
        else:  # just id
            parent = self.context
            new_id = path
        return Task(new_id, title, parent)
