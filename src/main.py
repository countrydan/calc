import sys

from rpn_builder import build_rpn
from reduce_rpn import reduce_rpn


if __name__ == "__main__":
    user_input = sys.argv[1]
    rpn = build_rpn(user_input)
    output = reduce_rpn(rpn)
    print(output)
