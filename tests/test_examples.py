"""
Integration tests: Running all example .jlt files.
"""

from pathlib import Path
from jlt.cli import run_file, check_file


def test_all_example_files():
    examples_dir = Path(__file__).parent.parent / "examples"
    example_files = sorted(examples_dir.glob("*.jlt"))

    assert len(example_files) >= 6, "Expected at least 6 example files!"

    for f in example_files:
        # Check syntax
        check_code = check_file(str(f))
        assert check_code == 0, f"Syntax check failed for {f.name}"

        # Execute file
        run_code = run_file(str(f))
        assert run_code == 0, f"Execution failed for {f.name}"
