from types import FunctionType
import inspect

from .helpers.func_helper import (
    create_func_from_src,
    get_clean_src_lines,
    get_modified_src_lines,
)
from .helpers.frame_helper import handle_frame
from .helpers.animate_helper import animate_frames

def animate(func):

    def wrapper(*args, **kwargs):

        # get globals() from caller module
        caller_globals = dict(inspect.getmembers(inspect.stack()[-1][0]))["f_globals"]

        __frames__ = []
        caller_globals["__frames__"] = __frames__
        caller_globals["handle_frame"] = handle_frame
        caller_globals["inspect"] = inspect

        src_lines: list[str] = get_clean_src_lines(func)
        mod_lines: list[str] = get_modified_src_lines(src_lines, caller_globals)

        newfunc = create_func_from_src("\n".join(mod_lines), caller_globals)

        # print("\n".join(mod_lines))

        output = newfunc(*args, **kwargs)

        animate_frames(__frames__, src_lines)

        return output
    
    return wrapper
