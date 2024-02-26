from numbers import Number

from src.rpn_builder import RPN, SYMBOLS

operations = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x * y,
    "/": lambda x, y: x / y,
    "^": lambda x, y: x**y,
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
        if item in SYMBOLS:
            try:
                y = stack.pop()
                x = stack.pop()
            except IndexError:
                raise Exception(f'Dangling expression: {' '.join(str(x) for x in rpn)}')
            operation = operations[item]
            stack.append(operation(x, y))

    return stack.pop()
