"""
Command Line Interface (CLI) for JLT (.jlt) language.
"""

import sys
import os
import argparse
from pathlib import Path

# Ensure UTF-8 output encoding for emojis and Unicode on Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter
from .transpiler import Transpiler
from .repl import start_repl
from .errors import JLTError

__version__ = "1.0.0"


def run_file(file_path: str) -> int:
    path = Path(file_path)
    if not path.exists():
        print(f"\n❌ [FILE NOT FOUND]: What ra, file '{file_path}' does not exist on this route!")
        return 1

    try:
        with open(path, "r", encoding="utf-8") as f:
            source = f.read()

        lexer = Lexer(source, str(path))
        tokens = lexer.tokenize()

        parser = Parser(tokens, source, str(path))
        program = parser.parse()

        interpreter = Interpreter(source, str(path))
        interpreter.interpret(program)
        return 0

    except JLTError as err:
        print(err.format_error())
        return 1
    except Exception as err:
        print(f"\n❌ [UNEXPECTED TRAFFIC JAM]: {err}")
        return 1


def check_file(file_path: str) -> int:
    path = Path(file_path)
    if not path.exists():
        print(f"\n❌ [FILE NOT FOUND]: What ra, file '{file_path}' does not exist!")
        return 1

    try:
        with open(path, "r", encoding="utf-8") as f:
            source = f.read()

        lexer = Lexer(source, str(path))
        tokens = lexer.tokenize()

        parser = Parser(tokens, source, str(path))
        program = parser.parse()

        print(f"✅ Pakka! '{file_path}' syntax is 100% valid Bangalore English code!")
        return 0

    except JLTError as err:
        print(err.format_error())
        return 1


def transpile_file(file_path: str, output_path: str = None) -> int:
    path = Path(file_path)
    if not path.exists():
        print(f"\n❌ [FILE NOT FOUND]: What ra, file '{file_path}' does not exist!")
        return 1

    try:
        with open(path, "r", encoding="utf-8") as f:
            source = f.read()

        lexer = Lexer(source, str(path))
        tokens = lexer.tokenize()

        parser = Parser(tokens, source, str(path))
        program = parser.parse()

        transpiler = Transpiler()
        py_code = transpiler.transpile(program)

        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(py_code)
            print(f"✅ Transpiled successfully to '{output_path}' boss!")
        else:
            print(py_code)
        return 0

    except JLTError as err:
        print(err.format_error())
        return 1


def main(argv=None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    if not argv:
        start_repl()
        return 0

    first_arg = argv[0]

    if first_arg in ("--version", "-v", "version"):
        print(f"Just Like That (.jlt) version {__version__} - Namma Bengaluru Edition 🚀")
        return 0

    if first_arg in ("repl", "shell", "interactive"):
        start_repl()
        return 0

    if first_arg == "run":
        if len(argv) < 2:
            print("Usage: jlt run <file.jlt>")
            return 1
        return run_file(argv[1])

    if first_arg == "check":
        if len(argv) < 2:
            print("Usage: jlt check <file.jlt>")
            return 1
        return check_file(argv[1])

    if first_arg == "transpile":
        if len(argv) < 2:
            print("Usage: jlt transpile <file.jlt> [-o output.py]")
            return 1
        out = None
        if len(argv) >= 4 and argv[2] in ("-o", "--output"):
            out = argv[3]
        return transpile_file(argv[1], out)

    # If it ends with .jlt or is a file, run it directly
    if first_arg.endswith(".jlt") or os.path.exists(first_arg):
        return run_file(first_arg)

    print(f"Unknown command: '{first_arg}'")
    print("Usage:")
    print("  jlt                   # Start interactive REPL")
    print("  jlt run <file.jlt>    # Execute a .jlt script")
    print("  jlt check <file.jlt>  # Validate syntax")
    print("  jlt transpile <file>  # Transpile to Python")
    return 1


if __name__ == "__main__":
    sys.exit(main())
