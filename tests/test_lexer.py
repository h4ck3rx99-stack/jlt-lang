"""
Tests for JLT Lexer / Tokenizer.
"""

import pytest
from jlt.lexer import Lexer
from jlt.tokens import TokenType
from jlt.errors import JLTSyntaxError


def test_lex_basic_tokens():
    source = 'let_us_say x = 100; pakka flag = pakka; bogus_flag = bogus;'
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    types = [t.type for t in tokens[:-1]] # exclude EOF
    assert types == [
        TokenType.LET_US_SAY,
        TokenType.IDENTIFIER,
        TokenType.ASSIGN,
        TokenType.NUMBER,
        TokenType.SEMICOLON,
        TokenType.BOOLEAN, # pakka const handled in parser
        TokenType.IDENTIFIER,
        TokenType.ASSIGN,
        TokenType.BOOLEAN,
        TokenType.SEMICOLON,
        TokenType.IDENTIFIER,
        TokenType.ASSIGN,
        TokenType.BOOLEAN,
        TokenType.SEMICOLON,
    ]


def test_lex_strings_with_escapes():
    source = r'tell_ra_macha("Hello \"Namma\" Bengaluru!\nSecond line");'
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    assert tokens[0].type == TokenType.TELL_RA_MACHA
    assert tokens[1].type == TokenType.LPAREN
    assert tokens[2].type == TokenType.STRING
    assert tokens[2].literal == 'Hello "Namma" Bengaluru!\nSecond line'


def test_lex_operators_and_bangalore_phrases():
    source = 'a same_to_same b and_also c more_than d'
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    types = [t.type for t in tokens[:-1]]
    assert types == [
        TokenType.IDENTIFIER,
        TokenType.EQ,
        TokenType.IDENTIFIER,
        TokenType.AND,
        TokenType.IDENTIFIER,
        TokenType.GT,
        TokenType.IDENTIFIER,
    ]


def test_lex_comments():
    source = """
    // Single line comment
    let_us_say x = 10; # Hash comment
    /* Multi
       line
       comment */
    tell_ra_macha(x);
    """
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    assert tokens[0].type == TokenType.LET_US_SAY
    assert tokens[1].type == TokenType.IDENTIFIER
    assert tokens[2].type == TokenType.ASSIGN
    assert tokens[3].type == TokenType.NUMBER
    assert tokens[4].type == TokenType.SEMICOLON
    assert tokens[5].type == TokenType.TELL_RA_MACHA


def test_lex_unterminated_string_error():
    source = 'tell_ra_macha("Unterminated string...'
    lexer = Lexer(source)
    with pytest.raises(JLTSyntaxError) as exc_info:
        lexer.tokenize()
    assert "Unterminated string" in str(exc_info.value)
