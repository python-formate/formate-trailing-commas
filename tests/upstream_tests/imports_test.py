# 3rd party
import pytest

# this package
from formate_trailing_commas import trailing_commas_hook


@pytest.mark.parametrize(
		"src",
		(
				'from os import path, makedirs\n',
				'from os import (path, makedirs)\n',
				'from os import (\n'
				'    path,\n'
				'    makedirs,\n'
				')',
				),
		)
def test_fix_from_import_noop(src):
	assert trailing_commas_hook(src, min_version=(2, 7)) == src


@pytest.mark.parametrize(
		("src", "expected"),
		(
				(
						'from os import (\n'
						'    makedirs,\n'
						'    path\n'
						')',
						'from os import (\n'
						'    makedirs,\n'
						'    path,\n'
						')',
						),
				(
						'from os import \\\n'
						'   (\n'
						'        path,\n'
						'        makedirs\n'
						'   )\n',
						'from os import \\\n'
						'   (\n'
						'        path,\n'
						'        makedirs,\n'
						'   )\n',
						),
				(
						'from os import (\n'
						'    makedirs,\n'
						'    path,\n'
						'    )',
						'from os import (\n'
						'    makedirs,\n'
						'    path,\n'
						')',
						),
				(
						'if True:\n'
						'    from os import (\n'
						'        makedirs\n'
						'    )',
						'if True:\n'
						'    from os import (\n'
						'        makedirs,\n'
						'    )',
						),
				),
		)
def test_fix_from_import(src, expected):
	assert trailing_commas_hook(src, min_version=(2, 7)) == expected
