# stdlib
import sys

# 3rd party
import pytest

# this package
from formate_trailing_commas import trailing_commas_hook

@pytest.mark.parametrize(
		's',
		(
				pytest.param(
						'match x:\n'
						'    case 1, 2:\n'
						'        pass\n',
						id="sequence without braces",
						),
				pytest.param(
						'match x:\n'
						'    case a():\n'
						'        pass\n',
						id="class without args",
						),
				),
		)
def test_noop_or_syntaxerror(s):
	if sys.version_info >= (3, 10):
		assert trailing_commas_hook(s, min_version=(2, 7)) == s
	else:
		with pytest.raises(SyntaxError, match="invalid syntax"):
			trailing_commas_hook(s, min_version=(2, 7))


@pytest.mark.xfail(sys.version_info < (3, 10), reason="py310+")
@pytest.mark.parametrize(
		("src", "expected"),
		(
				pytest.param(
						'match x:\n'
						'    case A(\n'
						'        1,\n'
						'        x=2\n'
						'    ):\n'
						'        pass\n',
						'match x:\n'
						'    case A(\n'
						'        1,\n'
						'        x=2,\n'
						'    ):\n'
						'        pass\n',
						id="match class",
						),
				pytest.param(
						'match x:\n'
						'    case (\n'
						'        1,\n'
						'        2\n'
						'    ):\n'
						'        pass\n',
						'match x:\n'
						'    case (\n'
						'        1,\n'
						'        2,\n'
						'    ):\n'
						'        pass\n',
						id="match sequence tuple",
						),
				pytest.param(
						'match x:\n'
						'    case (1, ):\n'
						'        pass\n',
						'match x:\n'
						'    case (1,):\n'
						'        pass\n',
						id="match sequence 1-element tuple",
						),
				pytest.param(
						'match x:\n'
						'    case [\n'
						'        1,\n'
						'        2\n'
						'    ]:\n'
						'        pass\n',
						'match x:\n'
						'    case [\n'
						'        1,\n'
						'        2,\n'
						'    ]:\n'
						'        pass\n',
						id="match sequence list",
						),
				pytest.param(
						'match x:\n'
						'    case [1, ]:\n'
						'        pass\n',
						'match x:\n'
						'    case [1]:\n'
						'        pass\n',
						id="match sequence list removes comma",
						),
				pytest.param(
						'match x:\n'
						'    case {\n'
						'        True: 1,\n'
						'        False: 2\n'
						'    }:\n'
						'        pass\n',
						'match x:\n'
						'    case {\n'
						'        True: 1,\n'
						'        False: 2,\n'
						'    }:\n'
						'        pass\n',
						id="match mapping",
						),
				pytest.param(
						'match x:\n'
						'    case {"x": 1,}:\n'
						'        pass\n',
						'match x:\n'
						'    case {"x": 1}:\n'
						'        pass\n',
						id="match mapping removes extra comma",
						),
				),
		)
def test_fix(src, expected):
	assert trailing_commas_hook(src, min_version=(2, 7)) == expected
