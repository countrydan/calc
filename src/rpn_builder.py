from enum import Enum, auto
from typing import NamedTuple
from collections import deque
import math


class MismatchedParentheses(Exception):
    """Raised when there is a dangling parentheses in the expression"""

    def __init__(self, user_input):
        super().__init__(f"Dangling parenthesis in expression: {user_input}")


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
SYMBOLS = ("+", "-", "*", "/", "^")
FUNCTIONS = ("log", "ln", "sin", "cos", "tan", "sqrt")
CONSTANTS = {"π": math.pi, "e": math.e}


def build_rpn(user_input: str) -> RPN:
    """
    Build reverse polish notation from an infix notation to handle easier calculations.

    :param user_input: infix notation input from user
    :return: list containing tokens in reverse polish notation
    """
    rpn: RPN = []
    operators: deque[str] = deque()

    tokens = tokenize(user_input)

    for token in tokens:
        if token.isnumeric() or "." in token or token in CONSTANTS:
            if "." in token:
                num = float(token)
            elif token in CONSTANTS:
                num = CONSTANTS[token]
            else:
                num = int(token)
            rpn.append(num)

        elif token in FUNCTIONS:
            operators.appendleft(token)

        elif token == "(":
            operators.appendleft(token)

        elif token in SYMBOLS:
            if operators:
                current_operator = precedence.get(token)
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
            operators.appendleft(token)

        elif token == ")":
            if not operators:
                raise MismatchedParentheses(user_input)
            while operators and operators[0] != "(":
                rpn.append(operators.popleft())
            if operators[0] == "(":
                operators.popleft()
            if operators and operators[0] in FUNCTIONS:
                rpn.append(operators.popleft())

    if "(" in operators:
        raise Exception("Dangling left parenthesis")

    rpn.extend(operators)
    return rpn


def tokenize(user_input: str) -> list[str]:
    """
    Tokenize user input into numbers and symbols.

    :param user_input: infix notation input from user
    :return: list of tokens of each number and symbol
    """
    tokens = []
    num_stack = ""

    for char in user_input:
        if char.isnumeric() or char == ".":
            num_stack += char
        elif char in SYMBOLS + ("(", ")"):
            if num_stack:
                tokens.append(num_stack)
                num_stack = ""
            tokens.append(char)
        elif char.isspace():
            continue
        else:
            raise Exception(f"Unknown mathematical token: {char}")
    if num_stack:
        tokens.append(num_stack)
    return tokens
