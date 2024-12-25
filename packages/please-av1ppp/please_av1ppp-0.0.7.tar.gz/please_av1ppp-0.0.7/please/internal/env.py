from os import environ
from pathlib import Path
from typing import Union

PathLike = Union[str, Path]


def parseenv(path: PathLike):
    env: dict[str, str] = dict()

    with open(path, mode="r") as file:
        for line in file.readlines():
            line = line.strip()
            if len(line) == 0 or line.startswith("#"):
                continue

            splitted = line.split("=", maxsplit=2)
            env[splitted[0].strip()] = splitted[1].strip()

    return env


def loadenv(path: PathLike):
    env = parseenv(path)
    for key, value in env.items():
        environ[key] = value
