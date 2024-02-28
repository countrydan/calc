from numbers import Number
import math

from src.rpn_builder import RPN


class InvalidExpression(Exception):
    """Raised when the expression is not valid"""

    def __init__(self, user_input):
        super().__init__(f"Invalid expression: {user_input}")


operations = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x * y,
    "/": lambda x, y: x / y,
    "^": lambda x, y: x**y,
}

functions = {
    "sin": lambda x: math.sin(math.radians(x)),
    "cos": lambda x: math.cos(math.radians(x)),
    "tan": lambda x: math.tan(math.radians(x)),
    "log": lambda x: math.log10(x),
    "ln": lambda x: math.log(x),
    "sqrt": lambda x: math.sqrt(x),
}


def reduce_rpn(rpn: RPN) -> int | float:
    """
    Reduce a reverse polish notation into a single number.

    :param rpn: list of numbers and operations in reverse polish notations
    :return: result of calculation
    """
    stack = []

    for item in rpn:
        if isinstance(item, Number):
            stack.append(item)
        if item in operations:
            try:
                y = stack.pop()
                x = stack.pop()
            except IndexError:
                raise InvalidExpression(" ".join(str(x) for x in rpn))
            operation = operations[item]
            stack.append(operation(x, y))
        elif item in functions:
            try:
                x = stack.pop()
            except IndexError:
                raise InvalidExpression(" ".join(str(x) for x in rpn))
            function = functions[item]
            stack.append(function(x))

    return stack.pop()
