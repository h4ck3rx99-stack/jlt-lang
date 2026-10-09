"""
Tests for JLT Parser.
"""

import pytest
from jlt.lexer import Lexer
from jlt.parser import Parser
from jlt.ast_nodes import (
    VarDeclStmt,
    IfStmt,
    WhileStmt,
    ForEachStmt,
    CountFromStmt,
    FuncDefStmt,
    TryCatchStmt,
    BinaryExpr,
    CallExpr,
)
from jlt.errors import JLTSyntaxError


def parse_snippet(source: str):
    tokens = Lexer(source).tokenize()
    return Parser(tokens, source).parse()


def test_parse_variable_declaration():
    prog = parse_snippet("let_us_say x = 42; fixed_boss pi = 3.14;")
    assert len(prog.statements) == 2
    assert isinstance(prog.statements[0], VarDeclStmt)
    assert prog.statements[0].name == "x"
    assert not prog.statements[0].is_const

    assert isinstance(prog.statements[1], VarDeclStmt)
    assert prog.statements[1].name == "pi"
    assert prog.statements[1].is_const


def test_parse_if_elif_else():
    source = """
    suppose (x > 10) {
        tell_ra_macha("Greater");
    } or_suppose (x == 10) {
        tell_ra_macha("Equal");
    } otherwise {
        tell_ra_macha("Lesser");
    }
    """
    prog = parse_snippet(source)
    assert len(prog.statements) == 1
    assert isinstance(prog.statements[0], IfStmt)
    assert len(prog.statements[0].elif_branches) == 1
    assert prog.statements[0].else_branch is not None


def test_parse_loops():
    source = """
    as_long_as (x > 0) { x = x - 1; }
    for_each item in [1, 2, 3] { tell_ra_macha(item); }
    count_from i = 1 to 10 step 2 { tell_ra_macha(i); }
    """
    prog = parse_snippet(source)
    assert len(prog.statements) == 3
    assert isinstance(prog.statements[0], WhileStmt)
    assert isinstance(prog.statements[1], ForEachStmt)
    assert isinstance(prog.statements[2], CountFromStmt)


def test_parse_functions():
    source = """
    do_one_thing add(a, b) {
        give_back a + b;
    }
    """
    prog = parse_snippet(source)
    assert len(prog.statements) == 1
    assert isinstance(prog.statements[0], FuncDefStmt)
    assert prog.statements[0].name == "add"
    assert prog.statements[0].params == ["a", "b"]


def test_parse_try_catch():
    source = """
    adjust_and_try {
        let_us_say x = 10 / 0;
    } what_ra_error (err) {
        tell_ra_macha("Handled: " + err);
    } in_the_end {
        tell_ra_macha("Done");
    }
    """
    prog = parse_snippet(source)
    assert len(prog.statements) == 1
    assert isinstance(prog.statements[0], TryCatchStmt)
    assert prog.statements[0].error_name == "err"
    assert prog.statements[0].finally_block is not None


def test_parse_syntax_error():
    source = "suppose (x > 5 {" # missing closing paren
    with pytest.raises(JLTSyntaxError):
        parse_snippet(source)
