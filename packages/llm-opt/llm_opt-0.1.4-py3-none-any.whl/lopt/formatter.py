import json as jsonlib
from typing import Any

import yaml as yamllib


def unordered_list(items: list[Any], *, bullet: str = "-") -> str:
    return "\n".join(f"{bullet} {item}" for item in items)


def ordered_list(items: list[Any], *, zero_indexed: bool = False) -> str:
    offset = not zero_indexed

    return "\n".join(f"{i + offset}. {item}" for i, item in enumerate(items))


def json(obj: Any, **dump_options: Any) -> str:
    return jsonlib.dumps(obj, **dump_options)


def yaml(obj: Any, **dump_options: Any) -> str:
    return yamllib.dump(obj, **dump_options)  # pyright: ignore[reportUnknownVariableType]
