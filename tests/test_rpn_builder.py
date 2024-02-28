import pytest
import math

from src.rpn_builder import build_rpn, tokenize


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
        ("100+500", [100, 500, "+"]),
        ("0.5 + 12 / 0.25", [0.5, 12, 0.25, "/", "+"]),
        ("sin ( log( 2 ) / 3 * π )", [2, "log", 3, "/", math.pi, "*", "sin"]),
    ],
)
def test_build_rpn(test_input, expected):
    rpn = build_rpn(test_input)
    assert rpn == expected


def test_build_rpn_fail_dangling_parentheses():
    with pytest.raises(Exception, match="Dangling parenthesis"):
        build_rpn("(1+1")


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("1+2", ["1", "+", "2"]),
        ("(1+2)-3", ["(", "1", "+", "2", ")", "-", "3"]),
        ("1+(1+(1-2))", ["1", "+", "(", "1", "+", "(", "1", "-", "2", ")", ")"]),
        ("100+500", ["100", "+", "500"]),
        (
            "100.25 * 15124.12467 / (1 + 3.5)",
            ["100.25", "*", "15124.12467", "/", "(", "1", "+", "3.5", ")"],
        ),
        ("sin(45)", ["sin", "(", "45", ")"]),
        (
            "sin ( max ( 2, 3 ) / 3 * π )",
            ["sin", "(", "max", "(", "2", ",", "3", ")", "/", "3", "*", "π", ")"],
        ),
    ],
)
def test_tokenize(test_input, expected):
    tokens = tokenize(test_input)
    assert expected == tokens


def test_unknown_token():
    with pytest.raises(Exception, match="Unknown mathematical token: @"):
        tokenize("@")
