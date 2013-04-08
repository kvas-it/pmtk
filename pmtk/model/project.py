"""
Project is the container for all other parts of the model
"""

from . import work
from .. import util


class Project(work.WorkBreakdownMixin, util.TitleMixin):

    def __init__(self, id, title=None):
        super(Project, self).__init__()
        self.id = id
        self.title = title
