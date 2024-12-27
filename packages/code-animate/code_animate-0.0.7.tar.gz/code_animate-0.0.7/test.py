from src.code_animate import animate, framify

def test1():
    return 1

def test2():
    return 2

def test3():
    return 3

@animate
def test():
    a = test1()
    b = test2()
    c = test3()

    output = a + b + c

    return output

print(test())
