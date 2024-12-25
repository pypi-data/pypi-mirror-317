from typing import List, Optional

from .argument import parse_args

_true_values = ["", "on", "yes", "y", "true"]
_false_values = ["off", "no", "n", "false"]


class TaskContext:
    def __init__(self, args: List[str]) -> None:
        self._args = parse_args(args)

    def args(self) -> List[str]:
        return list(
            map(
                lambda arg: arg.value,
                filter(
                    lambda arg: arg.key is None,
                    self._args,
                ),
            )
        )

    def string(self, key: str) -> Optional[str]:
        return self._find_by_key(key)

    def muststring(self, key: str):
        value = self.string(key)
        if value is None:
            raise Exception(f"argument '{key}' must be specified")
        return value

    def boolean(self, key: str) -> Optional[bool]:
        value = self._find_by_key(key)
        if value is None:
            return None
        if value in _true_values:
            return True
        elif value in _false_values:
            return False
        raise Exception(f"string '{value}' cannot be interpreted as a boolean value")

    def mustboolean(self, key: str):
        value = self.boolean(key)
        if value is None:
            raise Exception(f"argument '{key}' must be specified")
        return value

    def integer(self, key: str) -> Optional[int]:
        value = self._find_by_key(key)
        if value is None:
            return None
        try:
            value_ = int(value)
        except ValueError:
            raise Exception(f"string '{value}' cannot be interpreted as a int value")
        return value_

    def mustinteger(self, key: str):
        value = self.integer(key)
        if value is None:
            raise Exception(f"argument '{key}' must be specified")
        return value

    def float(self, key: str) -> Optional[float]:
        value = self._find_by_key(key)
        if value is None:
            return None
        try:
            value_ = float(value)
        except ValueError:
            raise Exception(f"string '{value}' cannot be interpreted as a float value")
        return value_

    def mustfloat(self, key: str):
        value = self.float(key)
        if value is None:
            raise Exception(f"argument '{key}' must be specified")
        return value

    def _find_by_key(self, key: str) -> Optional[str]:
        for arg in self._args:
            if arg.key == key:
                return arg.value
        return None
