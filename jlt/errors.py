"""
Bangalore English Error System for JLT.
Gives helpful, authentic Bangalore feedback when things go wrong in code!
"""

import sys
from typing import Optional


class JLTError(Exception):
    """Base error for all JLT language exceptions."""

    def __init__(
        self,
        message: str,
        line: Optional[int] = None,
        column: Optional[int] = None,
        source: Optional[str] = None,
        file_path: Optional[str] = None,
    ):
        super().__init__(message)
        self.message = message
        self.line = line
        self.column = column
        self.source = source
        self.file_path = file_path or "<namaskara_code>"

    def format_error(self) -> str:
        lines = []
        loc = f"{self.file_path}"
        if self.line is not None:
            loc += f":line {self.line}"
            if self.column is not None:
                loc += f":col {self.column}"

        lines.append(f"\n❌ [BANGALORE TRAFFIC ALERT / ERROR] at {loc}")
        lines.append(f"   What ra: {self.message}")

        if self.source and self.line is not None:
            source_lines = self.source.splitlines()
            if 1 <= self.line <= len(source_lines):
                code_line = source_lines[self.line - 1]
                lines.append("")
                lines.append(f"   {self.line:4d} | {code_line}")
                if self.column is not None and self.column >= 1:
                    pointer = " " * (self.column - 1) + "^"
                    lines.append(f"        | {pointer}")
                lines.append("")

        return "\n".join(lines)


class JLTSyntaxError(JLTError):
    """Raised when JLT parsing fails."""
    pass


class JLTRuntimeError(JLTError):
    """Raised during JLT execution."""
    pass


class JLTTypeError(JLTRuntimeError):
    """Raised when types don't match or invalid operation is attempted."""
    pass


class JLTNameError(JLTRuntimeError):
    """Raised when an identifier or variable is not found."""
    pass


class JLTZeroDivisionError(JLTRuntimeError):
    """Raised when division by zero occurs."""
    pass


# Bangalore-themed error quote helpers
BANGALORE_QUOTES = [
    "Swalpa adjust maadi boss!",
    "Silk Board traffic is faster than this bug!",
    "What macha, code broke like auto meter!",
    "Take one Filter Coffee and check line again da.",
    "Auto driver said 'Won't go there', interpreter said 'Won't run this'!",
    "No scene boss, just fix the typo and we are good to go!",
]
