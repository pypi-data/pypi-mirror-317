"""
helper functions related to creating function from string and vice versa
"""

from typing import Callable
from types import CodeType, FunctionType

def create_func_from_src(src: str) -> Callable:
    """
    Creates a function from source code

    Args:
        src (str): source code of function to create
    Returns
        Callable: function created from source code
    """
    module_code_obj: CodeType = compile(src, "<string>", "exec")

    # module_code_obj.co_const might have multiple objects due to type annotations
    # find the CodeType object and use it in FunctionType
    func_code_obj: FunctionType = None
    for value in module_code_obj.co_consts:
        if isinstance(value, CodeType):
            func_code_obj = value
            break
    
    func: FunctionType = FunctionType(func_code_obj, locals())

    return func

def add_line_dry_run_ok(
    existing_code_lines: list[str],
    new_line: str,
) -> bool:
    """
    Check if adding new_line to existing_code_lines result in error when compiling function

    Args:
        existing_code_lines (list[str]): list of code lines to try to run
        new_line (str): new line of code we are attempting to add to existing_code_lines
    
    Returns:
        (bool): if adding new_line causes compilation error, return False
                else, return True
    """
    # create source code
    src = "\n".join(existing_code_lines + [new_line])
    
    # try to create function from source code string
    try:
        create_func_from_src(src)
        return True
    except Exception as e:
        return False