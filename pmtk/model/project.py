"""
Project is the container for all other parts of the model
"""

from .work import WorkBreakdownMixin


class Project(WorkBreakdownMixin):

    def __init__(self, id, title=None):
        super(Project, self).__init__()
        self.id = id
        self.title = title

    def _getTitle(self):
        return self._title if self._title is not None else self.id

    def _setTitle(self, title):
        self._title = title

    title = property(_getTitle, _setTitle)
