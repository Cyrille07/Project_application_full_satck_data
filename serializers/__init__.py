from .employee import EmployeeOutput, EmployeeCreate, EmployeeOutputMini
from .task import TaskOutput, TaskCreate, TaskOutputMini

# résolution des types circulaires
TaskOutput.model_rebuild()
EmployeeOutput.model_rebuild()
