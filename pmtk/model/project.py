"""
Project is the container for all other parts of the model
"""

from .work import WorkBreakdownMixin
from .effort import EffortEstimatesMixin


class Project(WorkBreakdownMixin, EffortEstimatesMixin):

    def __init__(self, id, name=None):
        super(Project, self).__init__()
        self.id = id
        self.name = name if name is not None else id


