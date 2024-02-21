import sys
from enum import Enum, auto
from typing import NamedTuple

input = sys.argv[1]


class Associativity(Enum):
    LEFT = (auto(),)
    RIGHT = auto()


class Operator(NamedTuple):
    precedence: int
    associativity: Associativity


precedence: dict[str, Operator] = {
    "+": Operator(1, Associativity.LEFT),
    "-": Operator(1, Associativity.LEFT),
    "*": Operator(2, Associativity.LEFT),
    "/": Operator(2, Associativity.LEFT),
    "^": Operator(2, Associativity.RIGHT),
}

output: list[int | float | str] = []
operators: list[str] = []

# (1 * 2) - (3 * 4) -> 1 2 * 3 4 * -
# 1 + (1 + 1) * 5 -> 1 1 1 + 5 * +
"""
           there is an operator o2 at the top of the operator stack which is not a left parenthesis, 
            and (o2 has greater precedence than o1 or (o1 and o2 have the same precedence and o1 is left-associative))"""
for char in input:
    match char:
        case char if char.isnumeric():
            num = int(char) if "." or "," in char else float(char)  # TODO use result
            output.append(num)
        case char if char.isspace():
            continue
        case char if char == "(":
            operators.append(char)
        case char if char in ("+", "-", "*", "/", "^"):
            current_operator = precedence.get(char)  # TODO use result
            top_operator = precedence.get(operators[-1])
            while operators[-1] != "(" and (
                top_operator.precedence > current_operator.precedence
                or (
                    current_operator.precedence == top_operator.precedence
                    and current_operator.associativity == Associativity.LEFT
                )
            ):
                output.append(operators.pop())
                top_operator = precedence.get(operators[-1])
            operators.append(char)
        case char if char == ")":
            while (operator := operators.pop()) != "(":
                output.append(operator)
        case _:
            raise Exception(f"Unknown token: {char}")

if "(" in operators:
    raise Exception("Dangling left parenthesis")
output.extend(operators)
print(output)
# if char.isnumeric():
#     pass
# else:
#     operators.append(char)

# tokens.extend(operators)
#
# print(tokens)
#
# deck: deque[int | float] = deque()
#
# for token in tokens:
#     if not isinstance(token, str):
#         deck.append(token)
#     else:
#         x, y = deck.popleft(), deck.popleft()
#         match token:
#             case '+':
#                 result = x + y
#             case '-':
#                 result = x - y
#             case '/':
#                 result = x / y
#             case '*':
#                 result = x * y
#             case '(':
#
#             case _:
#                 raise Exception(f'Unknown operator: {token}')
#         deck.appendleft(result)
#
# print(deck)
