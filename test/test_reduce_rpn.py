import re

import pytest

from src.rpn_builder import build_rpn
from src.reduce_rpn import reduce_rpn


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("1+2", 3),
        ("(1+2)-3", 0),
        ("1+(1+(1-2))", 1),
        ("100+500", 600),
        (
            "0.1 * 10 / (0.5 + 3.5)",
            0.25,
        ),
        ("3 + 4 * 2 / ( 1 - 5 ) ^ 2 ^ 3", 3.000),
    ],
)
def test_reduce_rpn(test_input, expected):
    rpn = build_rpn(test_input)
    result = reduce_rpn(rpn)
    assert round(result, 3) == expected


def test_dangling_expression():
    with pytest.raises(Exception, match=re.escape("Dangling expression: 1 1 + +")):
        user_input = "1+1+"
        rpn = build_rpn(user_input)
        reduce_rpn(rpn)
