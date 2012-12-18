"""
$Id$

Project is the container for all other parts of the model
"""

from .work import WorkBreakdownMixin
from .effort import EffortEstimatesMixin


class Project(WorkBreakdownMixin, EffortEstimatesMixin):

    def __init__(self):
        super(Project, self).__init__()

