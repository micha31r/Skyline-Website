from background_task.models import Task
from .task_functions import remove_voided_tickets

# Repeat daily
remove_voided_tickets(repeat=Task.DAILY, repeat_until=None)