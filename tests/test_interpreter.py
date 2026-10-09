"""
Tests for JLT Interpreter and Runtime.
"""

import pytest
from jlt.lexer import Lexer
from jlt.parser import Parser
from jlt.interpreter import Interpreter
from jlt.errors import JLTRuntimeError, JLTZeroDivisionError, JLTNameError


def execute_source(source: str):
    tokens = Lexer(source).tokenize()
    prog = Parser(tokens, source).parse()
    interp = Interpreter(source)
    interp.interpret(prog)
    return interp


def test_eval_arithmetic_and_variables():
    source = """
    let_us_say a = 15;
    let_us_say b = 5;
    let_us_say sum = a + b;
    let_us_say diff = a - b;
    let_us_say prod = a * b;
    let_us_say quot = a / b;
    let_us_say power = 2 ^ 3;
    """
    interp = execute_source(source)
    assert interp.globals.get("sum") == 20
    assert interp.globals.get("diff") == 10
    assert interp.globals.get("prod") == 75
    assert interp.globals.get("quot") == 3.0
    assert interp.globals.get("power") == 8


def test_constants_cannot_be_reassigned():
    source = """
    pakka max_limit = 100;
    max_limit = 200;
    """
    with pytest.raises(JLTRuntimeError) as exc_info:
        execute_source(source)
    assert "Cannot reassign constant" in str(exc_info.value)


def test_functions_and_recursion():
    source = """
    do_one_thing factorial(n) {
        suppose (n <= 1) {
            give_back 1;
        }
        give_back n * factorial(n - 1);
    }
    let_us_say result = factorial(5);
    """
    interp = execute_source(source)
    assert interp.globals.get("result") == 120


def test_closures():
    source = """
    do_one_thing make_counter(start) {
        let_us_say count = start;
        do_one_thing increment() {
            count += 1;
            give_back count;
        }
        give_back increment;
    }
    let_us_say counter = make_counter(10);
    let_us_say c1 = counter();
    let_us_say c2 = counter();
    """
    interp = execute_source(source)
    assert interp.globals.get("c1") == 11
    assert interp.globals.get("c2") == 12


def test_try_catch_execution():
    source = """
    let_us_say caught_msg = "";
    let_us_say finalized = bogus;
    adjust_and_try {
        let_us_say bad = 10 / 0;
    } what_ra_error (err) {
        caught_msg = err;
    } in_the_end {
        finalized = pakka;
    }
    """
    interp = execute_source(source)
    assert "Division by zero" in interp.globals.get("caught_msg")
    assert interp.globals.get("finalized") is True


def test_lists_and_dicts():
    source = """
    let_us_say items = ["CTR", "MTR"];
    push(items, "Vidyarthi Bhavan");
    let_us_say count = len(items);

    let_us_say cafe = {
        "name": "Corner House",
        "speciality": "DBC"
    };
    let_us_say spec = cafe.speciality;
    """
    interp = execute_source(source)
    assert interp.globals.get("count") == 3
    assert interp.globals.get("spec") == "DBC"
