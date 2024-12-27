"""
helper functions relating to drawing code on terminal
"""

from typing import Any

from .classes import CodeLineToDraw

from colorama import Fore, Back

def draw_vars(var_dict: dict[str, Any]) -> str:
    """
    {"a": 4, "b": "apple"}

    To:

    a=4 b='apple' (with colour codes)
    """
    output_line: str = ""

    for key, val in var_dict.items():
        output_line += (
            Fore.RED + key + 
            Fore.WHITE + " = " +
            Fore.GREEN + repr(val) + 
            "  "
        )

    return output_line


def draw_code(
    codelines_to_draw: list[CodeLineToDraw],
    line_index: int,
) -> None:
    """
    Prints code in terminal + highlights current code line + prints variables that were changed

    Args:
        codelines_to_draw (list[CodeLineToDraw]): list of CodeLineToDraw objects
        line_index (int): index to highlight in green
    """
    longest_codeline_length = max([len(cl.line) for cl in codelines_to_draw])

    # RESET_ALL resets all foreground, background, whatever from colorama
    RESET_ALL: str = Fore.RESET + Back.RESET

    print(RESET_ALL)
    for index, codeline_to_draw in enumerate(codelines_to_draw):
        line_length: int = len(codeline_to_draw.line)
        padding = (longest_codeline_length - line_length + 2) * " " 

        if index == line_index:
            print(
                Fore.GREEN + 
                codeline_to_draw.line + 
                padding + 
                draw_vars(codeline_to_draw.vars)
            )
        else:
            print(
                RESET_ALL + 
                codeline_to_draw.line + 
                padding +
                draw_vars(codeline_to_draw.vars)
            )
    print(RESET_ALL)