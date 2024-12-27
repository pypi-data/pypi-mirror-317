from typing import Any

from .models import VarsDictAndLineNumberPair, AnimationLine

from unprint import unprint
from colorama import Fore, Back

RESET = Fore.RESET + Back.RESET

def animate_frames(
    frames: list[VarsDictAndLineNumberPair],
    src_lines: list[str],
) -> None:
    
    animation_lines: list[AnimationLine] = [
        AnimationLine(src_line=line, vars_dict={}) for line in src_lines
    ]

    current_items: dict = {}
    for vars_dict, line_num in frames:
        line_index: int = line_num - 1

        diff: dict[str, Any] = {
            k:v for k,v in vars_dict.items()
            if k not in current_items or v != current_items[k]
        }

        animation_lines[line_index].vars_dict = diff

        print()
        animate_once(animation_lines, line_index)
        print()
        input(">>>")
        unprint(len(src_lines)+3)
        current_items = vars_dict

    animate_once(animation_lines, line_index)

def animate_once(
    animation_lines: list[AnimationLine],
    line_index: int,
) -> None:

    max_length = max(len(al.src_line) for al in animation_lines)

    for index, animation_line in enumerate(animation_lines):
        src_line: str = animation_line.src_line
        vars_dict: dict[str, Any] = animation_line.vars_dict
        padding: str = (max_length - len(src_line) + 4) * " "

        if index == line_index:
            print(Fore.GREEN + src_line + padding + draw_vars(vars_dict))
        else:
            print(RESET + src_line + padding + draw_vars(vars_dict))

def draw_vars(vars_dict: dict[str, Any]) -> str:
    """
    {"a": 4, "b": "apple"}

    To:

    a=4 b='apple' (with colour codes)
    """
    output_line: str = ""
    for key, val in vars_dict.items():
        output_line += (
            Fore.RED + key + 
            Fore.WHITE + " = " +
            Fore.GREEN + repr(val) + 
            "  "
        )
    return output_line