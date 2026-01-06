#!/usr/bin/env python3
#
#  __init__.py
"""
Formate plugin to add trailing commas.
"""
#
#  Copyright © 2026 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
from ast import Tuple

# 3rd party
from tokenize_rt import src_to_tokens, tokens_to_src

# this package
from formate_trailing_commas._vendor.add_trailing_comma._ast_helpers import ast_parse
from formate_trailing_commas._vendor.add_trailing_comma._data import FUNCS, visit
from formate_trailing_commas._vendor.add_trailing_comma._main import _changing_list, _fix_src
from formate_trailing_commas._vendor.add_trailing_comma._token_helpers import START_BRACES, find_simple, fix_brace

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2026 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.0.0"
__email__: str = "dominic@davis-foster.co.uk"

__all__ = ["trailing_commas_hook"]


def trailing_commas_hook(source: str, **kwargs) -> str:
	r"""
	Call `add-trailing-comma <https://github.com/asottile/add-trailing-comma>`_, using the given keyword arguments as its configuration.

	:param source: The source to reformat.
	:param \*\*kwargs:

	:returns: The reformatted source.
	"""

	ast_obj = ast_parse(source)
	min_version: Tuple[int, int] = kwargs.get("min-version", (3, 6))

	callbacks = visit(FUNCS, ast_obj, min_version)

	tokens = src_to_tokens(source)
	for i, token in _changing_list(tokens):
		# DEDENT is a zero length token
		if not token.src:
			continue

		for callback in callbacks.get(token.offset, ()):
			callback(i, tokens)

		if token.src in START_BRACES:
			fix_brace(tokens, find_simple(i, tokens), add_comma=False, remove_comma=False)

	return tokens_to_src(tokens)
