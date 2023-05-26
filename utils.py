from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, NamedTuple, Tuple, TypeVar, Union, cast


def format_filter(attribute: str, value: str, operand: str = "="):
    return f"?filter[{attribute}][path]={attribute}&filter[{attribute}][value]{operand}{value}"
