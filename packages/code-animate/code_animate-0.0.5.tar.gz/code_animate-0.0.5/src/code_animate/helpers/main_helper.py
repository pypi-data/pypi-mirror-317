import re
from typing import Deque
from collections import deque

from .classes import CleanSrcDirtySrcPair
from .string_helper import get_indent
from .func_helper import add_line_dry_run_ok

def gen_clean_src_dirty_src_pair(src: str) -> CleanSrcDirtySrcPair:
    """
    Generate clean and dirty src from original src
    
    Args:
        src (str): source code of original function
    Returns:
        (CleanSrcDirtySrcPair): source code of new modified function
    """    
    # generate lines and remove empty lines
    orig_src_lines: Deque[str] = deque(
        line for line in src.split("\n")
    )

    # dirty/clean src must have same number of lines
    dirty_src_lines: list[str] = []
    clean_src_lines: list[str] = []

    # comment out all lines before 'def'
    while True:
        line: str = orig_src_lines.popleft()
        if re.match(r"def .*(.*):", line):
            dirty_src_lines.append(line)
            clean_src_lines.append(line)
            break
        else:
            dirty_src_lines.append("#" + line)
            clean_src_lines.append(line)

    # initialize frames: list[FrameType] in function
    indent: str = get_indent(orig_src_lines[0])
    dirty_src_lines.append(
        indent 
        + "__frames__ = [] ; from inspect import currentframe ; from default_deepcopy import default_deepcopy ; "
    )
    clean_src_lines.append(indent)

    # check if there is at least one return statement
    return_count: int = 0

    while orig_src_lines:
        line: str = orig_src_lines.popleft()

        if not line.strip():
            dirty_src_lines.append(line)
            clean_src_lines.append(line)
            continue

        # generate custom frame code
        indent: str = get_indent(line) 

        # if is return line
        if re.findall(r"\s+return .*", line):
            return_line: str = re.sub("return ", "return __frames__, ", line)
            dirty_src_lines.append(return_line)
            clean_src_lines.append(line)

            return_count += 1
        else: # currentframe ; from copy import deepcopy 
            frame_line: str = (
                line 
                + " ; __frame__ = currentframe()"
                + " ; __frames__.append([ "
                + "{k: default_deepcopy(v) for k,v in __frame__.f_locals.items() if '__frame' not in k}"
                + ", __frame__.f_lineno ])"
            )
            if add_line_dry_run_ok(dirty_src_lines, frame_line):
                dirty_src_lines.append(frame_line)
                clean_src_lines.append(line)
            else:
                dirty_src_lines.append(line)
                clean_src_lines.append(line)

    if return_count == 0:
        dirty_src_lines.append("    return __frames__, None")
        clean_src_lines.append("    ")

    dirty_src: str = "\n".join(dirty_src_lines).strip()
    clean_src: str = "\n".join(clean_src_lines).strip()

    return CleanSrcDirtySrcPair(
        clean_src=clean_src,
        dirty_src=dirty_src,
    )
