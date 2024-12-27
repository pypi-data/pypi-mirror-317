import re

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

def is_recursive(src: str) -> bool:
    func_name: str = re.findall(r"def (\w+)\(", src)[0]
    occurrences: list[str] = re.findall(rf"\W{func_name}\(", src)
    return len(occurrences) > 1