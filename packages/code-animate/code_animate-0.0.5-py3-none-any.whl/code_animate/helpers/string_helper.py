"""
Functions relating to string manipulation
"""

import re
from textwrap import dedent

from .exceptions import NotAFunctionException

def get_indent(line: str) -> str:
    """
    Get indent of string (leading spaces before first non-space character)
    """
    try:
        return re.findall(r"(\s+)\S", line)[0]
    except:
        return ""
    
def clean_up_src(src: str) -> str:
    """
    Cleans source code of a function
    """
    # unindent src in case it is indented
    src = dedent(src)

    # split src into list[str]
    src_lines: list[str] = src.split("\n")

    # remove all lines before def
    while True:
        if not src_lines:
            raise NotAFunctionException(f"Not a function: {src}")
        if re.findall(r" *def .*", src_lines[0]):
            break
        src_lines.pop(0)
        
    output_lines: list[str] = []

    for line in src_lines:

        # remove comments from line
        line: str = remove_comment_from_line(line)

        # skip if empty line
        if not line.strip():
            continue

        output_lines.append(line)

    return "\n".join(output_lines)


def remove_comment_from_line(line: str) -> str:
    """
    Removes comments from line of code, but not # in strings

    # hello world       => 
    print(123) # hello  => print(123)
    print('###') # hi   => print('###')
    """
    num_double_quotes: int = 0
    num_single_quotes: int = 0
    for index, char in enumerate(line):
        if index - 1 >= 0 and line[index] == "\\":
            # ignore if escape character
            continue
        elif char == "\"":
            num_double_quotes += 1
        elif char == "'":
            num_single_quotes += 1
        elif char == "#" and num_double_quotes % 2 == 0 and num_single_quotes % 2 == 0:
            return line[:index].rstrip()
    
    return line

