from typing import Callable

from .taskcontext import TaskContext

TaskFunc = Callable[[TaskContext], None]
