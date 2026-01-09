# 3rd party
import pytest

# this package
from formate_trailing_commas import trailing_commas_hook


@pytest.mark.parametrize(
		("src", "expected"),
		(
				# can't rewrite 1-element tuple
				("(1,)", "(1,)"),
				# but I do want the whitespace fixed!
				("(1, )", "(1,)"),
				("(1, 2,)", "(1, 2)"),
				("[1, 2,]", "[1, 2]"),
				("[1, 2,   ]", "[1, 2]"),
				("{1, 2, }", "{1, 2}"),
				("{1: 2, }", "{1: 2}"),
				("f(1, 2,)", "f(1, 2)"),
				),
		)
def test_remove_extra_comma(src, expected):
	assert trailing_commas_hook(src, min_version=(2, 7)) == expected
