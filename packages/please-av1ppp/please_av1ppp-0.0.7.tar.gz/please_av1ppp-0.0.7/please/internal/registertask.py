from typing import Optional

from .taskfunc import TaskFunc
from .tasks import tasks


def register_task(name: Optional[str] = None):
    def decorator(func: TaskFunc):
        nonlocal name

        if name is None:
            name = func.__name__

        if name in tasks:
            raise Exception(f"Task {name} already registered")

        tasks[name] = func

        # def wrapper() -> None:
        #     context = TaskContext()
        #     return func(context)

        # return wrapper
        return func

    return decorator
