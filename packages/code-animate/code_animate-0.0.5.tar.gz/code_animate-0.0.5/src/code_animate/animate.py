import re
from functools import wraps
from typing import Any, Callable, Sequence, Optional

from .helpers.draw_helper import draw_code
from .helpers.frame_helper import filter_framedict, compute_diff
from .helpers.classes import CodeLineToDraw
from .framify import framify

from unprint import unprint

def __wrapper_body(
    func: Callable,
    selected_keys: set[str],
    *args: Any,
    **kwargs: Any,
) -> Any:
    """
    Body of wrapper function
    """
    # framify original function
    newfunc = framify(func)

    # call modified function
    clean_src_lines, dirty_src_lines, frames, output = newfunc(*args, **kwargs)

    current_framedict: dict[str, Any] = {}

    # comments printed after codeline in terminal
    codelines_to_draw: list[CodeLineToDraw] = [
        CodeLineToDraw(line=line, comment="") 
        for line in clean_src_lines
    ]

    for framedict, line_number in frames:

        line_index: int = line_number - 1
        
        # filter wanted pairs in framedict eg. in selected_keys, meaningful values
        framedict: dict[str, Any] = filter_framedict(framedict, selected_keys)

        # compute difference between current_framedict and framedict
        diff: dict[str, Any] = compute_diff(current_framedict, framedict)

        # add comment to codelines_to_draw
        codelines_to_draw[line_index].comment = str(diff)

        draw_code(codelines_to_draw, line_index)
        
        input("\n>>>")
        unprint(len(clean_src_lines) + 5)

        current_framedict = framedict

    try:
        draw_code(codelines_to_draw, line_index)
    except: 
        pass

    return output


def animate(
    *args: Optional[Sequence[str | Callable]]
) -> Callable:
    """
    Animates your function step by step, printing changes in variables at each step

    Args
        *args (Optional[Sequence[str]]): 
            either:
                - variable names you want to focus on. Only these will be printed in animation
                - or function to decorate
    Returns
        (Callable) modified function with animation capabilities.
    """

    # if user just uses @animate
    if args and isinstance(args[0], Callable):
        func: Callable = args[0]
        @wraps(func)
        def wrapper(*args, **kwargs):
            return __wrapper_body(func, set(), *args, **kwargs)
        return wrapper

    selected_keys = {arg for arg in args if isinstance(arg, str)}

    # if user uses @animte("key1", "key2")
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            return __wrapper_body(func, selected_keys, *args, **kwargs)
        return wrapper

    return decorator
