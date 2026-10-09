"""
Abstract Syntax Tree (AST) Node definitions for JLT.
"""

from typing import Any, List, Optional, Tuple


class ASTNode:
    def __init__(self, line: int = 1, column: int = 1):
        self.line = line
        self.column = column

    def accept(self, visitor: Any) -> Any:
        method_name = f"visit_{self.__class__.__name__}"
        visitor_fn = getattr(visitor, method_name, None)
        if visitor_fn is None:
            raise NotImplementedError(f"No visitor method {method_name} found on {visitor.__class__.__name__}")
        return visitor_fn(self)


# ============================================================================
# Expressions
# ============================================================================

class Expr(ASTNode):
    pass


class LiteralExpr(Expr):
    def __init__(self, value: Any, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.value = value

    def __repr__(self) -> str:
        return f"Literal({self.value!r})"


class VarExpr(Expr):
    def __init__(self, name: str, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.name = name

    def __repr__(self) -> str:
        return f"Var({self.name})"


class UnaryExpr(Expr):
    def __init__(self, op: str, right: Expr, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.op = op
        self.right = right

    def __repr__(self) -> str:
        return f"Unary({self.op} {self.right})"


class BinaryExpr(Expr):
    def __init__(self, left: Expr, op: str, right: Expr, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self) -> str:
        return f"Binary({self.left} {self.op} {self.right})"


class LogicalExpr(Expr):
    def __init__(self, left: Expr, op: str, right: Expr, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self) -> str:
        return f"Logical({self.left} {self.op} {self.right})"


class CallExpr(Expr):
    def __init__(self, callee: Expr, args: List[Expr], line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.callee = callee
        self.args = args

    def __repr__(self) -> str:
        return f"Call({self.callee}({', '.join(map(str, self.args))}))"


class ListLiteralExpr(Expr):
    def __init__(self, elements: List[Expr], line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.elements = elements

    def __repr__(self) -> str:
        return f"List([{', '.join(map(str, self.elements))}])"


class DictLiteralExpr(Expr):
    def __init__(self, pairs: List[Tuple[Expr, Expr]], line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.pairs = pairs

    def __repr__(self) -> str:
        return f"Dict({self.pairs})"


class IndexExpr(Expr):
    def __init__(self, target: Expr, index: Expr, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.target = target
        self.index = index

    def __repr__(self) -> str:
        return f"Index({self.target}[{self.index}])"


class MemberExpr(Expr):
    def __init__(self, target: Expr, property_name: str, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.target = target
        self.property_name = property_name

    def __repr__(self) -> str:
        return f"Member({self.target}.{self.property_name})"


class AssignExpr(Expr):
    def __init__(self, target: Expr, value: Expr, op: str = "=", line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.target = target
        self.value = value
        self.op = op

    def __repr__(self) -> str:
        return f"Assign({self.target} {self.op} {self.value})"


# ============================================================================
# Statements
# ============================================================================

class Stmt(ASTNode):
    pass


class ExpressionStmt(Stmt):
    def __init__(self, expr: Expr, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.expr = expr

    def __repr__(self) -> str:
        return f"ExprStmt({self.expr})"


class VarDeclStmt(Stmt):
    def __init__(
        self,
        name: str,
        initializer: Optional[Expr],
        is_const: bool = False,
        line: int = 1,
        column: int = 1,
    ):
        super().__init__(line, column)
        self.name = name
        self.initializer = initializer
        self.is_const = is_const

    def __repr__(self) -> str:
        tag = "Const" if self.is_const else "Var"
        return f"{tag}Decl({self.name} = {self.initializer})"


class BlockStmt(Stmt):
    def __init__(self, statements: List[Stmt], line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.statements = statements

    def __repr__(self) -> str:
        return f"Block({len(self.statements)} stmts)"


class PrintStmt(Stmt):
    def __init__(self, args: List[Expr], line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.args = args

    def __repr__(self) -> str:
        return f"Print({self.args})"


class IfStmt(Stmt):
    def __init__(
        self,
        condition: Expr,
        then_branch: Stmt,
        elif_branches: List[Tuple[Expr, Stmt]],
        else_branch: Optional[Stmt] = None,
        line: int = 1,
        column: int = 1,
    ):
        super().__init__(line, column)
        self.condition = condition
        self.then_branch = then_branch
        self.elif_branches = elif_branches  # list of (cond, branch_stmt)
        self.else_branch = else_branch

    def __repr__(self) -> str:
        return f"If({self.condition}, elifs={len(self.elif_branches)}, has_else={self.else_branch is not None})"


class WhileStmt(Stmt):
    def __init__(self, condition: Expr, body: Stmt, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.condition = condition
        self.body = body

    def __repr__(self) -> str:
        return f"While({self.condition})"


class ForEachStmt(Stmt):
    def __init__(self, item_name: str, iterable: Expr, body: Stmt, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.item_name = item_name
        self.iterable = iterable
        self.body = body

    def __repr__(self) -> str:
        return f"ForEach({self.item_name} in {self.iterable})"


class CountFromStmt(Stmt):
    def __init__(
        self,
        var_name: str,
        start_expr: Expr,
        to_expr: Expr,
        step_expr: Optional[Expr],
        body: Stmt,
        line: int = 1,
        column: int = 1,
    ):
        super().__init__(line, column)
        self.var_name = var_name
        self.start_expr = start_expr
        self.to_expr = to_expr
        self.step_expr = step_expr
        self.body = body

    def __repr__(self) -> str:
        return f"CountFrom({self.var_name} = {self.start_expr} to {self.to_expr})"


class FuncDefStmt(Stmt):
    def __init__(
        self,
        name: str,
        params: List[str],
        body: BlockStmt,
        line: int = 1,
        column: int = 1,
    ):
        super().__init__(line, column)
        self.name = name
        self.params = params
        self.body = body

    def __repr__(self) -> str:
        return f"FuncDef({self.name}({', '.join(self.params)}))"


class ReturnStmt(Stmt):
    def __init__(self, value: Optional[Expr], line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.value = value

    def __repr__(self) -> str:
        return f"Return({self.value})"


class BreakStmt(Stmt):
    def __init__(self, line: int = 1, column: int = 1):
        super().__init__(line, column)

    def __repr__(self) -> str:
        return "Break()"


class ContinueStmt(Stmt):
    def __init__(self, line: int = 1, column: int = 1):
        super().__init__(line, column)

    def __repr__(self) -> str:
        return "Continue()"


class TryCatchStmt(Stmt):
    def __init__(
        self,
        try_block: Stmt,
        error_name: Optional[str],
        catch_block: Optional[Stmt],
        finally_block: Optional[Stmt],
        line: int = 1,
        column: int = 1,
    ):
        super().__init__(line, column)
        self.try_block = try_block
        self.error_name = error_name
        self.catch_block = catch_block
        self.finally_block = finally_block

    def __repr__(self) -> str:
        return f"TryCatch(err={self.error_name})"


class Program(ASTNode):
    def __init__(self, statements: List[Stmt], line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.statements = statements

    def __repr__(self) -> str:
        return f"Program({len(self.statements)} stmts)"
