from enum import Enum, auto
from typing import NamedTuple
from collections import deque


class Associativity(Enum):
    LEFT = auto()
    RIGHT = auto()


class Operator(NamedTuple):
    precedence: int
    associativity: Associativity


precedence: dict[str, Operator] = {
    "+": Operator(1, Associativity.LEFT),
    "-": Operator(1, Associativity.LEFT),
    "*": Operator(2, Associativity.LEFT),
    "/": Operator(2, Associativity.LEFT),
    "^": Operator(3, Associativity.RIGHT),
}

type RPN = list[int | float | str]


def build_rpn(user_input: str) -> RPN:
    """
    Build reverse polish notation from an infix notation to handle easier calculations.

    :param user_input: infix notation input from user
    :returns RPN: list containing tokens in reverse polish notation
    """
    rpn: RPN = []
    operators: deque[str] = deque()

    for char in user_input:
        match char:
            case char if char.isnumeric():
                num = int(char) if "." or "," in char else float(char)
                rpn.append(num)

            case char if char.isspace():
                continue

            case char if char == "(":
                operators.appendleft(char)

            case char if char in ("+", "-", "*", "/", "^"):
                if operators:
                    current_operator = precedence.get(char)
                    top_operator = precedence.get(operators[0])
                    while operators[0] != "(" and (
                        top_operator.precedence > current_operator.precedence
                        or (
                            current_operator.precedence == top_operator.precedence
                            and current_operator.associativity == Associativity.LEFT
                        )
                    ):
                        rpn.append(operators.popleft())
                        if operators:
                            top_operator = precedence.get(operators[0])
                        else:
                            break
                operators.appendleft(char)

            case char if char == ")":
                while (operator := operators.popleft()) != "(":
                    rpn.append(operator)

            case _:
                raise Exception(f"Unknown token: {char}")

    if "(" in operators:
        raise Exception("Dangling left parenthesis")

    rpn.extend(operators)
    return rpn
