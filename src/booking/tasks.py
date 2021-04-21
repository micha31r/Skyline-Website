from background_task.models import Task
from .task_functions import remove_expired_tickets

# Repeat daily
remove_expired_tickets(repeat=Task.DAILY, repeat_until=None)