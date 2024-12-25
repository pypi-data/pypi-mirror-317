from os import _Environ as Env
from pathlib import Path
from subprocess import run as subprocess_run
from sys import stderr, stdout
from typing import Dict, List, Optional, Union


def shexec(
    args: Union[Union[List[str], List[Path]], str, Path],
    env: Optional[Union[Env, Dict]] = None,
    cwd: Optional[Union[Path, str]] = None,
    timeout: Optional[float] = None,
    input: Optional[bytes] = None,
    capture_output: bool = False,
):
    return subprocess_run(
        check=True,
        input=input,
        timeout=timeout,
        args=_build_args(args),
        capture_output=capture_output,
        env=env,
        cwd=cwd,
        shell=True,
        stdout=None if capture_output else stdout,
        stderr=None if capture_output else stderr,
    )


def _build_args(args: Union[Union[List[str], List[Path]], str, Path]) -> str:
    if isinstance(args, str):
        return args
    if isinstance(args, Path):
        return str(args)
    if isinstance(args, list):
        cmd = ""
        for arg in args:
            cmd += str(arg) + " "
        return cmd
    raise TypeError("invalid args type")
