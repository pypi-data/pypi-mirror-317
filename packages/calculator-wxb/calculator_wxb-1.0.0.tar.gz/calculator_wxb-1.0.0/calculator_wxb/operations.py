def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y != 0:
        return x / y
    else:
        return "Error: Division by zero!"

def modulo(x, y):
    if y != 0:
        return x % y
    else:
        return "Error: Division by zero!"

def power(x, y):
    result = x
    for _ in range(y - 1):
        result *= x
    return result

def absolute(x):
    if x < 0:
        return -x
    else:
        return x

def bitwise_and(x, y):
    return x & y

def bitwise_or(x, y):
    return x | y

def bitwise_xor(x, y):
    return x ^ y

def bitwise_not(x):
    return -x - 1
