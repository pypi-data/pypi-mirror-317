
# code_animate
Allows you to animate your code step by step. 

Note - press Enter to conitnue to next step

# Installation
```
pip install code_animate
```

# Quickstart
```python
from code_animate import animate

@animate
def triangle(height: int) -> str:
    output: str = ""

    for i in range(height):
        num_stars: int = i + 1
        stars_str: str = "*" * num_stars
        output += stars_str + "\n"

    return output

print(triangle(4))

"""
def triangle(height: int) -> str:         
                                          
    output: str = ""                      {'height': 4, 'output': ''}
    for i in range(height):               
        num_stars: int = i + 1            {'i': 3, 'num_stars': 4}
        stars_str: str = "*" * num_stars  {'stars_str': '****'}
        output += stars_str + "\n"        {'output': '*\n**\n***\n****\n'}
    return output     
"""
```
