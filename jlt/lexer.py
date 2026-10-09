"""
Lexer (Tokenizer) for the JLT (.jlt) programming language.
"""

from typing import List, Optional
from .tokens import Token, TokenType, KEYWORDS
from .errors import JLTSyntaxError


class Lexer:
    def __init__(self, source: str, file_path: Optional[str] = None):
        self.source = source
        self.file_path = file_path or "<namaskara_code>"
        self.tokens: List[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.column = 1
        self.start_col = 1

    def tokenize(self) -> List[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.start_col = self.column
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line, self.column))
        return self.tokens

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def advance(self) -> str:
        char = self.source[self.current]
        self.current += 1
        self.column += 1
        return char

    def peek(self) -> str:
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        self.column += 1
        return True

    def add_token(self, type_: TokenType, literal: any = None) -> None:
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type_, text, literal, self.line, self.start_col))

    def scan_token(self) -> None:
        c = self.advance()

        if c in (" ", "\r", "\t"):
            # Whitespace
            pass
        elif c == "\n":
            self.line += 1
            self.column = 1
        elif c == "(":
            self.add_token(TokenType.LPAREN)
        elif c == ")":
            self.add_token(TokenType.RPAREN)
        elif c == "{":
            self.add_token(TokenType.LBRACE)
        elif c == "}":
            self.add_token(TokenType.RBRACE)
        elif c == "[":
            self.add_token(TokenType.LBRACKET)
        elif c == "]":
            self.add_token(TokenType.RBRACKET)
        elif c == ",":
            self.add_token(TokenType.COMMA)
        elif c == ";":
            self.add_token(TokenType.SEMICOLON)
        elif c == ":":
            self.add_token(TokenType.COLON)
        elif c == ".":
            self.add_token(TokenType.DOT)
        elif c == "+":
            if self.match("="):
                self.add_token(TokenType.PLUS_ASSIGN)
            else:
                self.add_token(TokenType.PLUS)
        elif c == "-":
            if self.match("="):
                self.add_token(TokenType.MINUS_ASSIGN)
            else:
                self.add_token(TokenType.MINUS)
        elif c == "*":
            self.add_token(TokenType.STAR)
        elif c == "%":
            self.add_token(TokenType.PERCENT)
        elif c == "^":
            self.add_token(TokenType.CARET)
        elif c == "/":
            if self.match("/"):
                # Single-line comment
                while self.peek() != "\n" and not self.is_at_end():
                    self.advance()
            elif self.match("*"):
                # Multi-line comment
                while not self.is_at_end():
                    if self.peek() == "*" and self.peek_next() == "/":
                        self.advance()
                        self.advance()
                        break
                    if self.peek() == "\n":
                        self.line += 1
                        self.column = 0
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)
        elif c == "#":
            # Hash single-line comment
            while self.peek() != "\n" and not self.is_at_end():
                self.advance()
        elif c == "!":
            if self.match("="):
                self.add_token(TokenType.NEQ)
            else:
                self.add_token(TokenType.NOT)
        elif c == "=":
            if self.match("="):
                self.add_token(TokenType.EQ)
            else:
                self.add_token(TokenType.ASSIGN)
        elif c == "<":
            if self.match("="):
                self.add_token(TokenType.LTE)
            else:
                self.add_token(TokenType.LT)
        elif c == ">":
            if self.match("="):
                self.add_token(TokenType.GTE)
            else:
                self.add_token(TokenType.GT)
        elif c == "&":
            if self.match("&"):
                self.add_token(TokenType.AND)
            else:
                raise JLTSyntaxError(
                    "Single '&' found! What ra, did you mean '&&' or 'and_also'?",
                    self.line,
                    self.start_col,
                    self.source,
                    self.file_path,
                )
        elif c == "|":
            if self.match("|"):
                self.add_token(TokenType.OR)
            else:
                raise JLTSyntaxError(
                    "Single '|' found! What ra, did you mean '||' or 'or_else'?",
                    self.line,
                    self.start_col,
                    self.source,
                    self.file_path,
                )
        elif c in ('"', "'"):
            self.scan_string(c)
        elif c.isdigit():
            self.scan_number()
        elif c.isalpha() or c == "_":
            self.scan_identifier()
        else:
            raise JLTSyntaxError(
                f"Unexpected character '{c}'! What macha, check your typing.",
                self.line,
                self.start_col,
                self.source,
                self.file_path,
            )

    def scan_string(self, quote_char: str) -> None:
        chars = []
        while self.peek() != quote_char and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
                self.column = 0
            if self.peek() == "\\":
                self.advance() # consume backslash
                if self.is_at_end():
                    break
                escaped = self.advance()
                if escaped == "n":
                    chars.append("\n")
                elif escaped == "t":
                    chars.append("\t")
                elif escaped == "r":
                    chars.append("\r")
                elif escaped == "\\":
                    chars.append("\\")
                elif escaped == '"':
                    chars.append('"')
                elif escaped == "'":
                    chars.append("'")
                else:
                    chars.append(escaped)
            else:
                chars.append(self.advance())

        if self.is_at_end():
            raise JLTSyntaxError(
                f"Unterminated string starting with {quote_char}! What ra, close your quote da!",
                self.line,
                self.start_col,
                self.source,
                self.file_path,
            )

        # Closing quote
        self.advance()
        string_val = "".join(chars)
        self.add_token(TokenType.STRING, string_val)

    def scan_number(self) -> None:
        while self.peek().isdigit():
            self.advance()

        # Look for fractional part
        if self.peek() == "." and self.peek_next().isdigit():
            self.advance() # consume '.'
            while self.peek().isdigit():
                self.advance()
            val = float(self.source[self.start:self.current])
        else:
            val = int(self.source[self.start:self.current])

        self.add_token(TokenType.NUMBER, val)

    def scan_identifier(self) -> None:
        while self.peek().isalnum() or self.peek() == "_":
            self.advance()

        text = self.source[self.start:self.current]

        # Check in keywords
        type_ = KEYWORDS.get(text)
        if type_ is None:
            # Regular user identifier
            self.add_token(TokenType.IDENTIFIER, text)
        elif type_ == TokenType.BOOLEAN:
            val = text in ("pakka", "correct_only", "true_da", "true")
            self.add_token(TokenType.BOOLEAN, val)
        elif type_ == TokenType.NULL:
            self.add_token(TokenType.NULL, None)
        else:
            self.add_token(type_, text)
