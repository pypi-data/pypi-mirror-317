from typing import NamedTuple, Any
from dataclasses import dataclass

class CleanSrcDirtySrcPair(NamedTuple):
    clean_src: str      # clean src to be printed during animation
    dirty_src: str      # modified src with inspect code

class InspectInfo(NamedTuple):
    clean_src_lines: list[str]      # clean src lines to be printed during animation
    dirty_src_lines: list[str]      # modified src with inspect code
    dict_line_number_pair: tuple[dict[str, Any], int] # (dict, line_number) pair
    output: Any                     # original output of function

@dataclass
class CodeLineToDraw:
    line: str       # actual code line
    comment: str    # printed afterwards
