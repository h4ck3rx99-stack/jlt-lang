"""
Tests for JLT Transpiler.
"""

from jlt.lexer import Lexer
from jlt.parser import Parser
from jlt.transpiler import Transpiler


def test_transpile_function_and_loop():
    source = """
    do_one_thing add(a, b) {
        give_back a + b;
    }
    let_us_say res = add(10, 20);
    tell_ra_macha("Result is: " + str(res));
    """
    tokens = Lexer(source).tokenize()
    prog = Parser(tokens, source).parse()
    py_code = Transpiler().transpile(prog)

    assert "def add(a, b):" in py_code
    assert "return (a + b)" in py_code
    assert "res = add(10, 20)" in py_code
    assert "tell_ra_macha(" in py_code

    # Execute transpiled code in Python
    local_scope = {}
    exec(py_code, local_scope)
    assert local_scope["res"] == 30
