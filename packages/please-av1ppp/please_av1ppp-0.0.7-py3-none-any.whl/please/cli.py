from pathlib import Path
from sys import argv, exit
from typing import Dict, Optional
import importlib
import sys

sys.path.append("./")

from pkg_resources import get_distribution

from .internal.taskcontext import TaskContext
from .internal.taskfunc import TaskFunc

dist = get_distribution("please_av1ppp")

pleasefile_module = "Pleasefile"
pleasefile_name = Path(pleasefile_module + ".py")


init_command = ["-i", "-init"]
help_command = ["-h", "-help"]
version_command = ["-v", "-version"]

help_indent = "    "


def main():
    tasks = get_tasks_from_pleasefile()
    args = argv[1:]

    if len(args) == 0 or args[0] in help_command:
        print_help(tasks)
        return

    if args[0] in init_command:
        init_pleasefile()
        return

    if args[0] in version_command:
        print_version()
        return

    if tasks is not None and args[0] in tasks:
        task = tasks[args[0]]
        ctx = TaskContext(args[1:])
        task(ctx)
        return

    panic(f"Command or task '{args[0]}' not found. Try to use -h command.")


def init_pleasefile():
    if pleasefile_name.exists():
        panic("Pleasefile already created")

    with open(pleasefile_name, mode="w") as file:
        file.write(
            """import please


@please.task()
def start(ctx: please.TaskContext):
    mode = ctx.string("mode") or "prod"
    print(f"*starting app in {mode} mode*")
"""
        )


def print_version():
    print("Please v" + dist.version)


def print_help(tasks: Optional[Dict[str, TaskFunc]]):
    print("PLEASE - simple task runner.")
    print()

    print("COMMANDS:")
    print_command(init_command, "Create empty Pleasefile")
    print_command(help_command, "Show this message")
    print_command(version_command, "Show version")

    if tasks is not None and len(tasks) > 0:
        print()
        print("TASKS:")
        for task_name, _ in tasks.items():
            print(f"{help_indent}{task_name}")


def get_tasks_from_pleasefile():
    try:
        module = importlib.import_module(pleasefile_module)
    except ModuleNotFoundError:
        return None

    try:
        tasks: Dict[str, TaskFunc] = module.please.internal.tasks.tasks
    except AttributeError:
        return None

    return tasks


def print_command(command: list, description: str):
    print(help_indent + ", ".join(command).ljust(26, " ") + description)


def panic(*values: object):
    print("ERROR:", *values)
    exit(1)


if __name__ == "__main__":
    main()
