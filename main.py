import sys
from collections import deque

input = sys.argv[1]

output: list[int | float | str] = []
operators: deque[str] = deque()

# (1 * 2) - (3 * 4) -> 1 2 * 3 4 * -
# 1 + (1 + 1) * 5 -> 1 1 1 + 5 * +
for char in input:
    match char:
        case char if char.isnumeric():
            num = int(char) if '.' or ',' in char else float(char) # TODO use result
            output.append(num)
        case char if char.isspace() or char == ',':
            continue
        case char if char in ('+', '-', '*', '/', '('):
            operators.appendleft(char)
        case char if char == ')':
            while (operator := operators.popleft()) != '(':
                output.append(operator)
        case _:
            raise Exception(f'Unknown token: {char}')

if '(' in operators:
    raise Exception('Dangling left parenthesis')
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
