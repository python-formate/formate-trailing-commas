# this package
from formate_trailing_commas import trailing_commas_hook


def test_problem_code():
	src = """
print(
		"Average build time:",
		f"{statistics.mean(build_times)}s,",
		f"σ {statistics.stdev(build_times)}",
		f"(n={len(build_times)})",
)
"""

	assert trailing_commas_hook(src) == src
