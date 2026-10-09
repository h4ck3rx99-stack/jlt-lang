"""
Interactive REPL (Read-Eval-Print Loop) for JLT (.jlt).
"""

import sys
from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter
from .errors import JLTError
from .builtins import jlt_format


BANNER = r"""
╔═════════════════════════════════════════════════════════════════════════════╗
║          ☕  JUST LIKE THAT (.jlt) - BANGALORE ENGLISH REPL  ☕             ║
║                                                                             ║
║   "Swalpa adjust maadi, code will run pakka boss!"                         ║
║   Type 'exit', 'pack_up_macha', or 'saaku' to leave the session.            ║
║   Sample: let_us_say x = 10; tell_ra_macha("Total: " + str(x * 2));         ║
╚═════════════════════════════════════════════════════════════════════════════╝
"""


def count_brackets(code: str) -> int:
    """Returns net balance of open braces/brackets/parentheses."""
    balance = 0
    in_str = False
    quote_char = ""
    i = 0
    while i < len(code):
        c = code[i]
        if in_str:
            if c == quote_char and (i == 0 or code[i - 1] != "\\"):
                in_str = False
        else:
            if c in ('"', "'"):
                in_str = True
                quote_char = c
            elif c in ("{", "(", "["):
                balance += 1
            elif c in ("}", ")", "]"):
                balance -= 1
        i += 1
    return balance


def start_repl() -> None:
    print(BANNER)
    interpreter = Interpreter(file_path="<repl>")

    buffer: list[str] = []

    while True:
        try:
            prompt = "jlt (bengaluru) >>> " if not buffer else "          ... >>> "
            line = input(prompt)

            clean_line = line.strip()
            if not buffer and clean_line in ("exit", "quit", "pack_up_macha", "saaku", "bye"):
                print("\nTata bye bye boss! See you at Corner House!\n")
                break

            buffer.append(line)
            combined = "\n".join(buffer)

            # Check if block is still open
            if count_brackets(combined) > 0:
                continue

            # Complete input ready to execute
            source = combined.strip()
            buffer.clear()

            if not source:
                continue

            lexer = Lexer(source, "<repl>")
            tokens = lexer.tokenize()
            parser = Parser(tokens, source, "<repl>")
            program = parser.parse()

            # Execute and if expression statement returned a value, display it nicely
            interpreter.source = source
            result = interpreter.interpret(program)
            if result is not None:
                print(f"➜ {jlt_format(result)}")

        except (KeyboardInterrupt, EOFError):
            print("\n\nTata bye bye boss! See you at CTR!\n")
            break
        except JLTError as err:
            buffer.clear()
            print(err.format_error())
        except Exception as err:
            buffer.clear()
            print(f"\n❌ [UNEXPECTED TRAFFIC JAM]: {err}\n")
