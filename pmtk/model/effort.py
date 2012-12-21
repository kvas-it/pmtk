"""
Classes related to effort estimation
"""


class EffortEstimatesMixin(object):
    """Container for the effort estimates (to be mixed into Project)"""

    def __init__(self):
        super(EffortEstimatesMixin, self).__init__()
        self.estimates = {}

    def addEstimate(self, task_id, man_hours):
        """Add effort estimate for the task"""
        self.estimates[task_id] = man_hours

    def getTaskEffort(self, task_id):
        """Return or calculate the effort for the task
        
        For tasks with no subtasks and not estimates returns zero.
        """
        if task_id in self.estimates:
            return self.estimates[task_id]
        else:
            return sum(self.getTaskEffort(subtask_id) for 
                    subtask_id in self.getSubtaskIds(task_id))

    def getTotalEffort(self):
        """Get the effort of the root task"""
        return self.getTaskEffort(self.getBreakdownRoot().id)

