
from typing import NamedTuple, Any
from dataclasses import dataclass

class VarsDictAndLineNumberPair(NamedTuple):
    vars_dict: dict[str, Any]
    line_number: int

@dataclass
class AnimationLine:
    src_line: str
    vars_dict: dict[str, Any]