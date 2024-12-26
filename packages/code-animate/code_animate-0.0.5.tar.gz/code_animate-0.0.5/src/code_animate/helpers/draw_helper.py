"""
helper functions relating to drawing code on terminal
"""

from colorama import Fore, Back

from .classes import CodeLineToDraw

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
                Fore.RED + 
                codeline_to_draw.comment
            )
        else:
            print(
                RESET_ALL + 
                codeline_to_draw.line + 
                padding +
                Fore.RED + codeline_to_draw.comment
            )
    print(RESET_ALL)