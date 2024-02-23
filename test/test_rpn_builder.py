import pytest

from src.rpn_builder import build_rpn


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("1+2", [1, 2, "+"]),
        ("1+2-3", [1, 2, "+", 3, "-"]),
        ("1+(1+(1-2))", [1, 1, 1, 2, "-", "+", "+"]),
        (
            "3 + 4 * 2 / ( 1 - 5 ) ^ 2 ^ 3",
            [3, 4, 2, "*", 1, 5, "-", 2, 3, "^", "^", "/", "+"],
        ),
    ],
)
def test_build_rpn(test_input, expected):
    rpn = build_rpn(test_input)
    assert rpn == expected


def test_build_rpn_fail_unknown_token():
    with pytest.raises(Exception, match="Unknown token: @"):
        build_rpn("@")


def test_build_rpn_fail_dangling_parentheses():
    with pytest.raises(Exception, match="Dangling left parenthesis"):
        build_rpn("(1+1")
