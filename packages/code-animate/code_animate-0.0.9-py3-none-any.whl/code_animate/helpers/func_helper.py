import re
import inspect
from collections.abc import Callable
from types import CodeType, FunctionType
from textwrap import dedent

from .string_helper import remove_comment_from_line, is_recursive

def get_clean_src_lines(func: Callable) -> list[str]:
    src_lines: list[str] = dedent(inspect.getsource(func)).split("\n")

    # remove all lines before 'def' keyword
    while True:
        if not src_lines:
            raise Exception(f"Not a function: {src_lines}")
        if re.findall(r" *def .*", src_lines[0]):
            break
        src_lines.pop(0)

    # remove empty lines
    out_src_lines: list[str] = []
    for line in src_lines:
        line: str = remove_comment_from_line(line)
        if line.strip():
            out_src_lines.append(line)
    return out_src_lines


def get_modified_src_lines(src_lines: list[str], desired_globals) -> list[str]:
    out: list[str] = []
    for line in src_lines:
        mod_line: str = line + " ; __frames__.append(handle_frame(inspect.currentframe()))"
        if add_line_dry_run_success(out, mod_line, desired_globals):
            out.append(mod_line)
        else:
            out.append(line)
    return out

def add_line_dry_run_success(src_lines, newline, desired_globals):
    src = "\n".join(src_lines + [newline])
    try:    # test if adding new line to existing src_lines works
        create_func_from_src(src, desired_globals)
        return True
    except Exception as e:
        # print(e)
        return False


def create_func_from_src(src: str, desired_globals: dict) -> Callable:
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
    return FunctionType(func_code_obj, desired_globals)
