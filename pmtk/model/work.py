"""
Classes related to work breakdown
"""

class Task:
    """Task is a basic element of work"""

    def __init__(self, id, title):
        self.id = id
        self.title = title
        self.subtask_ids = set()


ROOT_TASK_ID = 'MAIN'
ROOT_TASK_NAME = 'Main'

class WorkBreakdownMixin(object):
    """Container for the work breakdown (to be mixed into Project)"""

    def __init__(self):
        super(WorkBreakdownMixin, self).__init__()
        # root of the hierarchy of tasks
        self.root_task = Task(ROOT_TASK_ID, ROOT_TASK_NAME)
        # id -> task mapping
        self.tasks = {ROOT_TASK_ID: self.root_task}

    def addTask(self, id, name=None, parent=ROOT_TASK_ID):
        """Add a new task to the work breakdown"""
        if id in self.tasks:
            raise ValueError('Duplicate task id: %s' % id)
        if parent not in self.tasks:
            raise ValueError('Parent task id (%s) does not exist' % id)
        self.tasks[id] = Task(id, name if name is not None else id)
        self.tasks[parent].subtask_ids.add(id)

    def getSubtaskIds(self, task_id):
        return self.tasks[task_id].subtask_ids

    def getBreakdownRoot(self):
        return self.root_task

    def getTaskById(self, id):
        return self.tasks[id]

