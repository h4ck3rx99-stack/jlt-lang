"""
Token definitions and Bangalore English keyword mappings for JLT (.jlt).
"""

from enum import Enum, auto
from typing import Any, Optional


class TokenType(Enum):
    # Literals
    NUMBER = auto()
    STRING = auto()
    BOOLEAN = auto()
    NULL = auto()
    IDENTIFIER = auto()

    # Keywords - Variables & Constants
    LET_US_SAY = auto()       # let_us_say, put, macha, boss, da, guru
    PAKKA_CONST = auto()      # fixed_boss, solid, constant_macha, fixed_guru

    # Keywords - I/O
    TELL_RA_MACHA = auto()    # tell_ra_macha, tell_da, shout, heli_guru, display_macha
    ASK_MACHA = auto()        # ask_macha, ask_da, what_ra_input, kelu_macha

    # Keywords - Conditionals
    SUPPOSE = auto()          # suppose, suppose_if, what_if, nod_macha
    OR_SUPPOSE = auto()       # or_suppose, what_if_scene_is, otherwise_suppose, matthe_nod_macha
    OTHERWISE = auto()        # otherwise, or_else_macha, simply, illa_andre

    # Keywords - Loops
    AS_LONG_AS = auto()       # as_long_as, keep_doing, traffic_loop, allivargu
    FOR_EACH = auto()         # for_each, each_and_every
    IN = auto()               # in, alli
    COUNT_FROM = auto()       # count_from, round_haku
    TO = auto()               # to, varge
    STEP = auto()             # step, jump
    PACK_UP_MACHA = auto()    # pack_up_macha, saaku_boss, break_da, saaku_macha
    ADJUST_AND_GO = auto()    # adjust_and_go, skip_da, next_da, mundhe_hogo

    # Keywords - Functions
    DO_ONE_THING = auto()     # do_one_thing, the_plan_is, what_to_do, matter_enu_andre
    GIVE_BACK = auto()        # give_back, take_macha, return_da, kodu_macha

    # Keywords - Error Handling
    ADJUST_AND_TRY = auto()   # adjust_and_try, try_maadi, chill_and_try, adjust_madu
    WHAT_RA_ERROR = auto()    # what_ra_error, ayyo_problem, ayyo_rama
    IN_THE_END = auto()       # in_the_end, lastly, final_agi, konege

    # Operators - Comparison
    EQ = auto()               # ==, same_to_same, ditto
    NEQ = auto()              # !=, different_only, not_same
    GT = auto()               # >, more_than, jaasti
    LT = auto()               # <, less_than, kammi
    GTE = auto()              # >=, atleast, jaasti_illa_equal
    LTE = auto()              # <=, atmost, kammi_illa_equal

    # Operators - Logical
    AND = auto()              # &&, and_also, matthe
    OR = auto()               # ||, or_else, athava
    NOT = auto()              # !, opposite, ulta, not_only

    # Operators - Arithmetic
    PLUS = auto()             # +
    MINUS = auto()            # -
    STAR = auto()             # *
    SLASH = auto()            # /
    PERCENT = auto()          # %
    CARET = auto()            # ^ (exponent)
    ASSIGN = auto()           # =
    PLUS_ASSIGN = auto()      # +=
    MINUS_ASSIGN = auto()     # -=

    # Delimiters
    LPAREN = auto()           # (
    RPAREN = auto()           # )
    LBRACE = auto()           # {
    RBRACE = auto()           # }
    LBRACKET = auto()         # [
    RBRACKET = auto()         # ]
    COMMA = auto()            # ,
    SEMICOLON = auto()        # ;
    COLON = auto()            # :
    DOT = auto()              # .

    # Special
    EOF = auto()


class Token:
    def __init__(
        self,
        type_: TokenType,
        lexeme: str,
        literal: Any = None,
        line: int = 1,
        column: int = 1,
    ):
        self.type = type_
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
        self.column = column

    def __repr__(self) -> str:
        if self.literal is not None:
            return f"Token({self.type.name}, {self.lexeme!r}, {self.literal!r}, L{self.line}:{self.column})"
        return f"Token({self.type.name}, {self.lexeme!r}, L{self.line}:{self.column})"


# Bangalore English & Kanglish keyword lookup table
KEYWORDS = {
    # Variables
    "let_us_say": TokenType.LET_US_SAY,
    "put": TokenType.LET_US_SAY,
    "macha": TokenType.LET_US_SAY,
    "boss": TokenType.LET_US_SAY,
    "da": TokenType.LET_US_SAY,
    "guru": TokenType.LET_US_SAY,
    "let": TokenType.LET_US_SAY,
    "var": TokenType.LET_US_SAY,

    # Constants
    "fixed_boss": TokenType.PAKKA_CONST,
    "solid": TokenType.PAKKA_CONST,
    "constant_macha": TokenType.PAKKA_CONST,
    "fixed_guru": TokenType.PAKKA_CONST,
    "const": TokenType.PAKKA_CONST,

    # Output / Print
    "tell_ra_macha": TokenType.TELL_RA_MACHA,
    "tell_da": TokenType.TELL_RA_MACHA,
    "tell_boss": TokenType.TELL_RA_MACHA,
    "shout": TokenType.TELL_RA_MACHA,
    "heli_guru": TokenType.TELL_RA_MACHA,
    "display_macha": TokenType.TELL_RA_MACHA,
    "print": TokenType.TELL_RA_MACHA,

    # Input
    "ask_macha": TokenType.ASK_MACHA,
    "ask_da": TokenType.ASK_MACHA,
    "what_ra_input": TokenType.ASK_MACHA,
    "kelu_macha": TokenType.ASK_MACHA,
    "input": TokenType.ASK_MACHA,

    # Conditionals
    "suppose": TokenType.SUPPOSE,
    "suppose_if": TokenType.SUPPOSE,
    "what_if": TokenType.SUPPOSE,
    "nod_macha": TokenType.SUPPOSE,
    "scene_iddre": TokenType.SUPPOSE,
    "if": TokenType.SUPPOSE,

    "or_suppose": TokenType.OR_SUPPOSE,
    "what_if_scene_is": TokenType.OR_SUPPOSE,
    "otherwise_suppose": TokenType.OR_SUPPOSE,
    "matthe_nod_macha": TokenType.OR_SUPPOSE,
    "bere_scene_iddre": TokenType.OR_SUPPOSE,
    "elif": TokenType.OR_SUPPOSE,
    "else_if": TokenType.OR_SUPPOSE,

    "otherwise": TokenType.OTHERWISE,
    "or_else_macha": TokenType.OTHERWISE,
    "simply": TokenType.OTHERWISE,
    "illa_andre": TokenType.OTHERWISE,
    "scene_illandre": TokenType.OTHERWISE,
    "else": TokenType.OTHERWISE,

    # Loops
    "as_long_as": TokenType.AS_LONG_AS,
    "keep_doing": TokenType.AS_LONG_AS,
    "traffic_loop": TokenType.AS_LONG_AS,
    "allivargu": TokenType.AS_LONG_AS,
    "while": TokenType.AS_LONG_AS,

    "for_each": TokenType.FOR_EACH,
    "each_and_every": TokenType.FOR_EACH,
    "for": TokenType.FOR_EACH,

    "in": TokenType.IN,
    "alli": TokenType.IN,

    "count_from": TokenType.COUNT_FROM,
    "round_haku": TokenType.COUNT_FROM,

    "to": TokenType.TO,
    "varge": TokenType.TO,

    "step": TokenType.STEP,

    "pack_up_macha": TokenType.PACK_UP_MACHA,
    "saaku_boss": TokenType.PACK_UP_MACHA,
    "break_da": TokenType.PACK_UP_MACHA,
    "saaku_macha": TokenType.PACK_UP_MACHA,
    "packup_guru": TokenType.PACK_UP_MACHA,
    "break": TokenType.PACK_UP_MACHA,

    "adjust_and_go": TokenType.ADJUST_AND_GO,
    "skip_da": TokenType.ADJUST_AND_GO,
    "next_da": TokenType.ADJUST_AND_GO,
    "mundhe_hogo": TokenType.ADJUST_AND_GO,
    "continue": TokenType.ADJUST_AND_GO,

    # Functions
    "do_one_thing": TokenType.DO_ONE_THING,
    "the_plan_is": TokenType.DO_ONE_THING,
    "what_to_do": TokenType.DO_ONE_THING,
    "matter_enu_andre": TokenType.DO_ONE_THING,
    "plan_enu_andre": TokenType.DO_ONE_THING,
    "func": TokenType.DO_ONE_THING,
    "def": TokenType.DO_ONE_THING,
    "function": TokenType.DO_ONE_THING,

    "give_back": TokenType.GIVE_BACK,
    "take_macha": TokenType.GIVE_BACK,
    "return_da": TokenType.GIVE_BACK,
    "kodu_macha": TokenType.GIVE_BACK,
    "idko_macha": TokenType.GIVE_BACK,
    "return": TokenType.GIVE_BACK,

    # Error Handling
    "adjust_and_try": TokenType.ADJUST_AND_TRY,
    "try_maadi": TokenType.ADJUST_AND_TRY,
    "chill_and_try": TokenType.ADJUST_AND_TRY,
    "adjust_madu": TokenType.ADJUST_AND_TRY,
    "try": TokenType.ADJUST_AND_TRY,

    "what_ra_error": TokenType.WHAT_RA_ERROR,
    "ayyo_problem": TokenType.WHAT_RA_ERROR,
    "ayyo_rama": TokenType.WHAT_RA_ERROR,
    "ayyo_catch": TokenType.WHAT_RA_ERROR,
    "catch": TokenType.WHAT_RA_ERROR,
    "except": TokenType.WHAT_RA_ERROR,

    "in_the_end": TokenType.IN_THE_END,
    "lastly": TokenType.IN_THE_END,
    "final_agi": TokenType.IN_THE_END,
    "konege": TokenType.IN_THE_END,
    "finally": TokenType.IN_THE_END,

    # Comparison Keywords
    "same_to_same": TokenType.EQ,
    "ditto": TokenType.EQ,
    "different_only": TokenType.NEQ,
    "not_same": TokenType.NEQ,
    "more_than": TokenType.GT,
    "jaasti": TokenType.GT,
    "less_than": TokenType.LT,
    "kammi": TokenType.LT,
    "atleast": TokenType.GTE,
    "jaasti_illa_equal": TokenType.GTE,
    "atmost": TokenType.LTE,
    "kammi_illa_equal": TokenType.LTE,

    # Logical Keywords
    "and_also": TokenType.AND,
    "matthe": TokenType.AND,
    "and": TokenType.AND,

    "or_else": TokenType.OR,
    "athava": TokenType.OR,
    "or": TokenType.OR,

    "opposite": TokenType.NOT,
    "ulta": TokenType.NOT,
    "not_only": TokenType.NOT,
    "not": TokenType.NOT,

    # Literals
    "pakka": TokenType.BOOLEAN, # handled: boolean True by default, or constant if before identifier in decl
    "correct_only": TokenType.BOOLEAN,
    "true_da": TokenType.BOOLEAN,
    "true": TokenType.BOOLEAN,

    "bogus": TokenType.BOOLEAN,
    "fake_news": TokenType.BOOLEAN,
    "wrong_only": TokenType.BOOLEAN,
    "illa": TokenType.BOOLEAN,
    "false": TokenType.BOOLEAN,

    "khali": TokenType.NULL,
    "empty_scene": TokenType.NULL,
    "nothing_da": TokenType.NULL,
    "null": TokenType.NULL,
    "none": TokenType.NULL,
    "nil": TokenType.NULL,
}
