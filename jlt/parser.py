"""
Recursive descent Parser for the JLT (.jlt) programming language.
"""

from typing import List, Optional, Tuple
from .tokens import Token, TokenType
from .ast_nodes import (
    ASTNode,
    Program,
    Stmt,
    Expr,
    LiteralExpr,
    VarExpr,
    UnaryExpr,
    BinaryExpr,
    LogicalExpr,
    CallExpr,
    ListLiteralExpr,
    DictLiteralExpr,
    IndexExpr,
    MemberExpr,
    AssignExpr,
    ExpressionStmt,
    VarDeclStmt,
    BlockStmt,
    PrintStmt,
    IfStmt,
    WhileStmt,
    ForEachStmt,
    CountFromStmt,
    FuncDefStmt,
    ReturnStmt,
    BreakStmt,
    ContinueStmt,
    TryCatchStmt,
)
from .errors import JLTSyntaxError


class Parser:
    def __init__(self, tokens: List[Token], source: str, file_path: Optional[str] = None):
        self.tokens = tokens
        self.source = source
        self.file_path = file_path or "<namaskara_code>"
        self.current = 0

    def parse(self) -> Program:
        statements: List[Stmt] = []
        while not self.is_at_end():
            # Skip stray semicolons
            if self.match(TokenType.SEMICOLON):
                continue
            stmt = self.declaration()
            if stmt is not None:
                statements.append(stmt)
        return Program(statements, 1, 1)

    # -------------------------------------------------------------------------
    # Helper Navigation Methods
    # -------------------------------------------------------------------------

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.EOF

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def check(self, type_: TokenType) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type == type_

    def match(self, *types: TokenType) -> bool:
        for t in types:
            if self.check(t):
                self.advance()
                return True
        return False

    def consume(self, type_: TokenType, message: str) -> Token:
        if self.check(type_):
            return self.advance()
        token = self.peek()
        raise JLTSyntaxError(
            f"{message} (Got {token.lexeme!r})",
            token.line,
            token.column,
            self.source,
            self.file_path,
        )

    def match_semicolon(self) -> None:
        """Optional semicolon consumed if present."""
        self.match(TokenType.SEMICOLON)

    # -------------------------------------------------------------------------
    # Declarations & Statements
    # -------------------------------------------------------------------------

    def declaration(self) -> Stmt:
        try:
            if self.match(TokenType.LET_US_SAY):
                return self.var_declaration(is_const=False)
            if self.match(TokenType.PAKKA_CONST):
                return self.var_declaration(is_const=True)
            # Handle 'pakka' when used as constant declaration if followed by identifier and '='
            if self.check(TokenType.BOOLEAN) and self.peek().lexeme == "pakka":
                if self.current + 1 < len(self.tokens) and self.tokens[self.current + 1].type == TokenType.IDENTIFIER:
                    self.advance() # consume 'pakka'
                    return self.var_declaration(is_const=True)
            if self.match(TokenType.DO_ONE_THING):
                return self.func_declaration()
            return self.statement()
        except JLTSyntaxError:
            self.synchronize()
            raise

    def var_declaration(self, is_const: bool) -> VarDeclStmt:
        start_tok = self.previous()
        name_tok = self.consume(
            TokenType.IDENTIFIER,
            "What ra, variable name missing! Provide a valid variable name da."
        )
        initializer = None
        if self.match(TokenType.ASSIGN):
            initializer = self.expression()
        elif is_const:
            raise JLTSyntaxError(
                f"Constant '{name_tok.lexeme}' must be initialized boss! No khali constants allowed.",
                name_tok.line,
                name_tok.column,
                self.source,
                self.file_path,
            )
        self.match_semicolon()
        return VarDeclStmt(name_tok.lexeme, initializer, is_const, start_tok.line, start_tok.column)

    def func_declaration(self) -> FuncDefStmt:
        start_tok = self.previous()
        name_tok = self.consume(
            TokenType.IDENTIFIER,
            "What macha, function name is missing! What to do without a name?"
        )
        self.consume(
            TokenType.LPAREN,
            "Expected '(' after function name boss!"
        )
        params: List[str] = []
        if not self.check(TokenType.RPAREN):
            while True:
                p_tok = self.consume(
                    TokenType.IDENTIFIER,
                    "Expected parameter name in function definition."
                )
                params.append(p_tok.lexeme)
                if not self.match(TokenType.COMMA):
                    break
        self.consume(TokenType.RPAREN, "Expected ')' after parameters list.")
        self.consume(TokenType.LBRACE, "Expected '{' to start function body.")
        body = self.block_statement()
        return FuncDefStmt(name_tok.lexeme, params, body, start_tok.line, start_tok.column)

    def statement(self) -> Stmt:
        if self.match(TokenType.TELL_RA_MACHA):
            return self.print_statement()
        if self.match(TokenType.SUPPOSE):
            return self.if_statement()
        if self.match(TokenType.AS_LONG_AS):
            return self.while_statement()
        if self.match(TokenType.FOR_EACH):
            return self.for_each_statement()
        if self.match(TokenType.COUNT_FROM):
            return self.count_from_statement()
        if self.match(TokenType.ADJUST_AND_TRY):
            return self.try_catch_statement()
        if self.match(TokenType.GIVE_BACK):
            return self.return_statement()
        if self.match(TokenType.PACK_UP_MACHA):
            tok = self.previous()
            self.match_semicolon()
            return BreakStmt(tok.line, tok.column)
        if self.match(TokenType.ADJUST_AND_GO):
            tok = self.previous()
            self.match_semicolon()
            return ContinueStmt(tok.line, tok.column)
        if self.match(TokenType.LBRACE):
            return self.block_statement()
        return self.expression_statement()

    def print_statement(self) -> PrintStmt:
        start_tok = self.previous()
        self.consume(TokenType.LPAREN, "Expected '(' after tell_ra_macha / print keyword.")
        args: List[Expr] = []
        if not self.check(TokenType.RPAREN):
            while True:
                args.append(self.expression())
                if not self.match(TokenType.COMMA):
                    break
        self.consume(TokenType.RPAREN, "Expected ')' after tell_ra_macha arguments.")
        self.match_semicolon()
        return PrintStmt(args, start_tok.line, start_tok.column)

    def if_statement(self) -> IfStmt:
        start_tok = self.previous()
        self.consume(TokenType.LPAREN, "Expected '(' after suppose / condition keyword.")
        condition = self.expression()
        self.consume(TokenType.RPAREN, "Expected ')' after suppose condition.")
        then_branch = self.statement()

        elif_branches: List[Tuple[Expr, Stmt]] = []
        while self.match(TokenType.OR_SUPPOSE):
            self.consume(TokenType.LPAREN, "Expected '(' after or_suppose condition.")
            elif_cond = self.expression()
            self.consume(TokenType.RPAREN, "Expected ')' after or_suppose condition.")
            elif_branch = self.statement()
            elif_branches.append((elif_cond, elif_branch))

        else_branch = None
        if self.match(TokenType.OTHERWISE):
            else_branch = self.statement()

        return IfStmt(condition, then_branch, elif_branches, else_branch, start_tok.line, start_tok.column)

    def while_statement(self) -> WhileStmt:
        start_tok = self.previous()
        self.consume(TokenType.LPAREN, "Expected '(' after as_long_as / loop keyword.")
        condition = self.expression()
        self.consume(TokenType.RPAREN, "Expected ')' after loop condition.")
        body = self.statement()
        return WhileStmt(condition, body, start_tok.line, start_tok.column)

    def for_each_statement(self) -> ForEachStmt:
        start_tok = self.previous()
        item_tok = self.consume(
            TokenType.IDENTIFIER,
            "Expected item variable name in for_each loop."
        )
        self.consume(
            TokenType.IN,
            "Expected 'in' or 'alli' after item name in for_each loop."
        )
        iterable = self.expression()
        body = self.statement()
        return ForEachStmt(item_tok.lexeme, iterable, body, start_tok.line, start_tok.column)

    def count_from_statement(self) -> CountFromStmt:
        start_tok = self.previous()
        var_tok = self.consume(
            TokenType.IDENTIFIER,
            "Expected counter variable name in count_from loop."
        )
        self.consume(TokenType.ASSIGN, "Expected '=' after counter variable name.")
        start_expr = self.expression()
        self.consume(TokenType.TO, "Expected 'to' or 'varge' in count_from loop.")
        to_expr = self.expression()
        step_expr = None
        if self.match(TokenType.STEP):
            step_expr = self.expression()
        body = self.statement()
        return CountFromStmt(var_tok.lexeme, start_expr, to_expr, step_expr, body, start_tok.line, start_tok.column)

    def try_catch_statement(self) -> TryCatchStmt:
        start_tok = self.previous()
        try_block = self.statement()
        error_name = None
        catch_block = None

        if self.match(TokenType.WHAT_RA_ERROR):
            if self.match(TokenType.LPAREN):
                err_tok = self.consume(
                    TokenType.IDENTIFIER,
                    "Expected error variable name inside '(' after what_ra_error."
                )
                error_name = err_tok.lexeme
                self.consume(TokenType.RPAREN, "Expected ')' after error variable.")
            catch_block = self.statement()

        finally_block = None
        if self.match(TokenType.IN_THE_END):
            finally_block = self.statement()

        if catch_block is None and finally_block is None:
            raise JLTSyntaxError(
                "adjust_and_try must have at least one what_ra_error or in_the_end block boss!",
                start_tok.line,
                start_tok.column,
                self.source,
                self.file_path,
            )

        return TryCatchStmt(try_block, error_name, catch_block, finally_block, start_tok.line, start_tok.column)

    def return_statement(self) -> ReturnStmt:
        start_tok = self.previous()
        value = None
        if not self.check(TokenType.SEMICOLON) and not self.check(TokenType.RBRACE):
            value = self.expression()
        self.match_semicolon()
        return ReturnStmt(value, start_tok.line, start_tok.column)

    def block_statement(self) -> BlockStmt:
        start_tok = self.previous()
        statements: List[Stmt] = []
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            if self.match(TokenType.SEMICOLON):
                continue
            stmt = self.declaration()
            if stmt is not None:
                statements.append(stmt)
        self.consume(TokenType.RBRACE, "Expected '}' to close block! Traffic jam in braces!")
        return BlockStmt(statements, start_tok.line, start_tok.column)

    def expression_statement(self) -> ExpressionStmt:
        expr = self.expression()
        self.match_semicolon()
        return ExpressionStmt(expr, expr.line, expr.column)

    # -------------------------------------------------------------------------
    # Expressions & Precedence
    # -------------------------------------------------------------------------

    def expression(self) -> Expr:
        return self.assignment()

    def assignment(self) -> Expr:
        expr = self.logical_or()

        if self.match(TokenType.ASSIGN, TokenType.PLUS_ASSIGN, TokenType.MINUS_ASSIGN):
            op_tok = self.previous()
            value = self.assignment()

            if isinstance(expr, (VarExpr, IndexExpr, MemberExpr)):
                return AssignExpr(expr, value, op_tok.lexeme, op_tok.line, op_tok.column)

            raise JLTSyntaxError(
                f"Invalid assignment target! What ra, you cannot assign to {expr}!",
                op_tok.line,
                op_tok.column,
                self.source,
                self.file_path,
            )

        return expr

    def logical_or(self) -> Expr:
        expr = self.logical_and()
        while self.match(TokenType.OR):
            op = self.previous().lexeme
            right = self.logical_and()
            expr = LogicalExpr(expr, op, right, expr.line, expr.column)
        return expr

    def logical_and(self) -> Expr:
        expr = self.equality()
        while self.match(TokenType.AND):
            op = self.previous().lexeme
            right = self.equality()
            expr = LogicalExpr(expr, op, right, expr.line, expr.column)
        return expr

    def equality(self) -> Expr:
        expr = self.comparison()
        while self.match(TokenType.EQ, TokenType.NEQ):
            op = self.previous().lexeme
            right = self.comparison()
            expr = BinaryExpr(expr, op, right, expr.line, expr.column)
        return expr

    def comparison(self) -> Expr:
        expr = self.term()
        while self.match(TokenType.GT, TokenType.GTE, TokenType.LT, TokenType.LTE):
            op = self.previous().lexeme
            right = self.term()
            expr = BinaryExpr(expr, op, right, expr.line, expr.column)
        return expr

    def term(self) -> Expr:
        expr = self.factor()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = self.previous().lexeme
            right = self.factor()
            expr = BinaryExpr(expr, op, right, expr.line, expr.column)
        return expr

    def factor(self) -> Expr:
        expr = self.power()
        while self.match(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            op = self.previous().lexeme
            right = self.power()
            expr = BinaryExpr(expr, op, right, expr.line, expr.column)
        return expr

    def power(self) -> Expr:
        expr = self.unary()
        while self.match(TokenType.CARET):
            op = self.previous().lexeme
            right = self.unary()
            expr = BinaryExpr(expr, op, right, expr.line, expr.column)
        return expr

    def unary(self) -> Expr:
        if self.match(TokenType.NOT, TokenType.MINUS, TokenType.PLUS):
            op_tok = self.previous()
            right = self.unary()
            return UnaryExpr(op_tok.lexeme, right, op_tok.line, op_tok.column)
        return self.call()

    def call(self) -> Expr:
        expr = self.primary()

        while True:
            if self.match(TokenType.LPAREN):
                expr = self.finish_call(expr)
            elif self.match(TokenType.LBRACKET):
                index = self.expression()
                self.consume(TokenType.RBRACKET, "Expected ']' after index subscript.")
                expr = IndexExpr(expr, index, expr.line, expr.column)
            elif self.match(TokenType.DOT):
                prop_tok = self.consume(
                    TokenType.IDENTIFIER,
                    "Expected property name after '.' boss!"
                )
                expr = MemberExpr(expr, prop_tok.lexeme, expr.line, expr.column)
            else:
                break

        return expr

    def finish_call(self, callee: Expr) -> CallExpr:
        args: List[Expr] = []
        if not self.check(TokenType.RPAREN):
            while True:
                args.append(self.expression())
                if not self.match(TokenType.COMMA):
                    break
        paren = self.consume(TokenType.RPAREN, "Expected ')' after arguments.")
        return CallExpr(callee, args, paren.line, paren.column)

    def primary(self) -> Expr:
        tok = self.peek()

        if self.match(TokenType.BOOLEAN):
            return LiteralExpr(self.previous().literal, tok.line, tok.column)

        if self.match(TokenType.NULL):
            return LiteralExpr(None, tok.line, tok.column)

        if self.match(TokenType.NUMBER, TokenType.STRING):
            return LiteralExpr(self.previous().literal, tok.line, tok.column)

        if self.match(TokenType.ASK_MACHA):
            # Built-in input expression: ask_macha("prompt")
            prompt_expr = None
            if self.match(TokenType.LPAREN):
                if not self.check(TokenType.RPAREN):
                    prompt_expr = self.expression()
                self.consume(TokenType.RPAREN, "Expected ')' after ask_macha.")
            return CallExpr(VarExpr("ask_macha", tok.line, tok.column), [prompt_expr] if prompt_expr else [], tok.line, tok.column)

        if self.match(TokenType.IDENTIFIER):
            return VarExpr(self.previous().lexeme, tok.line, tok.column)

        if self.match(TokenType.LPAREN):
            expr = self.expression()
            self.consume(TokenType.RPAREN, "Expected ')' after group expression.")
            return expr

        # List Literal: [1, 2, 3]
        if self.match(TokenType.LBRACKET):
            start_tok = self.previous()
            elements: List[Expr] = []
            if not self.check(TokenType.RBRACKET):
                while True:
                    elements.append(self.expression())
                    if not self.match(TokenType.COMMA):
                        break
            self.consume(TokenType.RBRACKET, "Expected ']' to close list literal.")
            return ListLiteralExpr(elements, start_tok.line, start_tok.column)

        # Dictionary / Object Literal: {"key": value, ...}
        if self.match(TokenType.LBRACE):
            start_tok = self.previous()
            pairs: List[Tuple[Expr, Expr]] = []
            if not self.check(TokenType.RBRACE):
                while True:
                    key = self.expression()
                    self.consume(TokenType.COLON, "Expected ':' between key and value in dictionary.")
                    val = self.expression()
                    pairs.append((key, val))
                    if not self.match(TokenType.COMMA):
                        break
            self.consume(TokenType.RBRACE, "Expected '}' to close dictionary literal.")
            return DictLiteralExpr(pairs, start_tok.line, start_tok.column)

        raise JLTSyntaxError(
            f"Unexpected token '{tok.lexeme}'! What ra, syntax error here only!",
            tok.line,
            tok.column,
            self.source,
            self.file_path,
        )

    def synchronize(self) -> None:
        self.advance()
        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return
            if self.peek().type in (
                TokenType.LET_US_SAY,
                TokenType.PAKKA_CONST,
                TokenType.DO_ONE_THING,
                TokenType.SUPPOSE,
                TokenType.AS_LONG_AS,
                TokenType.FOR_EACH,
                TokenType.COUNT_FROM,
                TokenType.ADJUST_AND_TRY,
                TokenType.TELL_RA_MACHA,
                TokenType.GIVE_BACK,
            ):
                return
            self.advance()
