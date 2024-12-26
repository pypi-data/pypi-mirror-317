

from src.code_animate import animate

@animate
def triangle(height: int) -> str:
    output: str = ""

    for i in range(height):
        num_stars: int = i + 1
        stars_str: str = "*" * num_stars
        output += stars_str + "\n"

    return output

print(triangle(4))
