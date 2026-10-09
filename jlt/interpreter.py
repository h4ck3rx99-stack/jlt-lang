"""
Tree-walking Interpreter and Runtime Environment for JLT (.jlt).
"""

from typing import Any, Callable, Dict, List, Optional, Set
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
from .errors import (
    JLTError,
    JLTRuntimeError,
    JLTTypeError,
    JLTNameError,
    JLTZeroDivisionError,
)
from .builtins import get_default_builtins, jlt_format


class ReturnSignal(Exception):
    def __init__(self, value: Any):
        self.value = value


class BreakSignal(Exception):
    pass


class ContinueSignal(Exception):
    pass


class Environment:
    def __init__(self, enclosing: Optional["Environment"] = None):
        self.values: Dict[str, Any] = {}
        self.constants: Set[str] = set()
        self.enclosing = enclosing

    def define(self, name: str, value: Any, is_const: bool = False) -> None:
        self.values[name] = value
        if is_const:
            self.constants.add(name)

    def assign(
        self,
        name: str,
        value: Any,
        line: int = 1,
        column: int = 1,
        source: Optional[str] = None,
        file_path: Optional[str] = None,
    ) -> None:
        if name in self.values:
            if name in self.constants:
                raise JLTRuntimeError(
                    f"Cannot reassign constant '{name}'! Pakka means pakka boss, fixed value!",
                    line,
                    column,
                    source,
                    file_path,
                )
            self.values[name] = value
            return

        if self.enclosing is not None:
            self.enclosing.assign(name, value, line, column, source, file_path)
            return

        raise JLTNameError(
            f"Variable '{name}' not found! What ra, did you forget to declare it with 'let_us_say {name} = ...'?",
            line,
            column,
            source,
            file_path,
        )

    def get(
        self,
        name: str,
        line: int = 1,
        column: int = 1,
        source: Optional[str] = None,
        file_path: Optional[str] = None,
    ) -> Any:
        if name in self.values:
            return self.values[name]

        if self.enclosing is not None:
            return self.enclosing.get(name, line, column, source, file_path)

        raise JLTNameError(
            f"Variable '{name}' is not defined! What macha, where did '{name}' come from?",
            line,
            column,
            source,
            file_path,
        )


class JLTCallable:
    def call(self, interpreter: "Interpreter", arguments: List[Any], line: int = 1, column: int = 1) -> Any:
        raise NotImplementedError()


class JLTFunction(JLTCallable):
    def __init__(self, declaration: FuncDefStmt, closure: Environment):
        self.declaration = declaration
        self.closure = closure

    def call(self, interpreter: "Interpreter", arguments: List[Any], line: int = 1, column: int = 1) -> Any:
        expected_count = len(self.declaration.params)
        if len(arguments) != expected_count:
            raise JLTTypeError(
                f"Function '{self.declaration.name}' expects {expected_count} arguments, but got {len(arguments)}! Swalpa adjust maadi boss!",
                line,
                column,
                interpreter.source,
                interpreter.file_path,
            )

        environment = Environment(self.closure)
        for param, arg in zip(self.declaration.params, arguments):
            environment.define(param, arg)

        try:
            interpreter.execute_block(self.declaration.body.statements, environment)
        except ReturnSignal as ret:
            return ret.value

        return None

    def __repr__(self) -> str:
        return f"<function {self.declaration.name}>"


class JLTBuiltinWrapper(JLTCallable):
    def __init__(self, name: str, fn: Callable):
        self.name = name
        self.fn = fn

    def call(self, interpreter: "Interpreter", arguments: List[Any], line: int = 1, column: int = 1) -> Any:
        try:
            return self.fn(*arguments)
        except JLTError as e:
            if e.line is None:
                e.line = line
                e.column = column
                e.source = interpreter.source
                e.file_path = interpreter.file_path
            raise e
        except TypeError as e:
            raise JLTTypeError(
                f"Built-in function '{self.name}' error: {e}",
                line,
                column,
                interpreter.source,
                interpreter.file_path,
            )
        except Exception as e:
            raise JLTRuntimeError(
                f"Error in '{self.name}': {e}",
                line,
                column,
                interpreter.source,
                interpreter.file_path,
            )

    def __repr__(self) -> str:
        return f"<builtin_function {self.name}>"


class Interpreter:
    def __init__(self, source: str = "", file_path: Optional[str] = None):
        self.source = source
        self.file_path = file_path or "<namaskara_code>"
        self.globals = Environment()
        self.environment = self.globals
        self._init_builtins()

    def _init_builtins(self) -> None:
        for name, fn in get_default_builtins().items():
            self.globals.define(name, JLTBuiltinWrapper(name, fn))

    def interpret(self, program: Program) -> Any:
        try:
            result = None
            for stmt in program.statements:
                result = self.execute(stmt)
            return result
        except ReturnSignal as ret:
            return ret.value

    def execute(self, stmt: Stmt) -> Any:
        return stmt.accept(self)

    def evaluate(self, expr: Expr) -> Any:
        return expr.accept(self)

    def execute_block(self, statements: List[Stmt], environment: Environment) -> None:
        previous = self.environment
        try:
            self.environment = environment
            for stmt in statements:
                self.execute(stmt)
        finally:
            self.environment = previous

    # =========================================================================
    # Statements Visitors
    # =========================================================================

    def visit_Program(self, node: Program) -> Any:
        result = None
        for stmt in node.statements:
            result = self.execute(stmt)
        return result

    def visit_ExpressionStmt(self, node: ExpressionStmt) -> Any:
        return self.evaluate(node.expr)

    def visit_VarDeclStmt(self, node: VarDeclStmt) -> None:
        val = None
        if node.initializer is not None:
            val = self.evaluate(node.initializer)
        self.environment.define(node.name, val, is_const=node.is_const)

    def visit_BlockStmt(self, node: BlockStmt) -> None:
        self.execute_block(node.statements, Environment(self.environment))

    def visit_PrintStmt(self, node: PrintStmt) -> None:
        values = [self.evaluate(arg) for arg in node.args]
        formatted = " ".join(jlt_format(v) for v in values)
        print(formatted)

    def visit_IfStmt(self, node: IfStmt) -> None:
        if self.is_truthy(self.evaluate(node.condition)):
            self.execute(node.then_branch)
            return

        for elif_cond, elif_branch in node.elif_branches:
            if self.is_truthy(self.evaluate(elif_cond)):
                self.execute(elif_branch)
                return

        if node.else_branch is not None:
            self.execute(node.else_branch)

    def visit_WhileStmt(self, node: WhileStmt) -> None:
        while self.is_truthy(self.evaluate(node.condition)):
            try:
                self.execute(node.body)
            except BreakSignal:
                break
            except ContinueSignal:
                continue

    def visit_ForEachStmt(self, node: ForEachStmt) -> None:
        iterable = self.evaluate(node.iterable)
        if not isinstance(iterable, (list, str, dict, tuple)):
            raise JLTTypeError(
                f"What ra! Cannot loop over '{type(iterable).__name__}' with for_each!",
                node.line,
                node.column,
                self.source,
                self.file_path,
            )

        for item in iterable:
            loop_env = Environment(self.environment)
            loop_env.define(node.item_name, item)
            try:
                if isinstance(node.body, BlockStmt):
                    self.execute_block(node.body.statements, loop_env)
                else:
                    prev = self.environment
                    try:
                        self.environment = loop_env
                        self.execute(node.body)
                    finally:
                        self.environment = prev
            except BreakSignal:
                break
            except ContinueSignal:
                continue

    def visit_CountFromStmt(self, node: CountFromStmt) -> None:
        start_val = self.evaluate(node.start_expr)
        to_val = self.evaluate(node.to_expr)
        step_val = self.evaluate(node.step_expr) if node.step_expr else 1

        if not isinstance(start_val, (int, float)) or not isinstance(to_val, (int, float)):
            raise JLTTypeError(
                "What macha, count_from boundaries must be numbers!",
                node.line,
                node.column,
                self.source,
                self.file_path,
            )

        cur = int(start_val)
        target = int(to_val)
        step = int(step_val)

        if step == 0:
            raise JLTRuntimeError("Step in count_from cannot be 0! Infinite traffic jam!", node.line, node.column, self.source, self.file_path)

        def condition(c: int) -> bool:
            return c <= target if step > 0 else c >= target

        while condition(cur):
            loop_env = Environment(self.environment)
            loop_env.define(node.var_name, cur)
            try:
                if isinstance(node.body, BlockStmt):
                    self.execute_block(node.body.statements, loop_env)
                else:
                    prev = self.environment
                    try:
                        self.environment = loop_env
                        self.execute(node.body)
                    finally:
                        self.environment = prev
            except BreakSignal:
                break
            except ContinueSignal:
                pass
            cur += step

    def visit_FuncDefStmt(self, node: FuncDefStmt) -> None:
        fn = JLTFunction(node, self.environment)
        self.environment.define(node.name, fn)

    def visit_ReturnStmt(self, node: ReturnStmt) -> None:
        value = None
        if node.value is not None:
            value = self.evaluate(node.value)
        raise ReturnSignal(value)

    def visit_BreakStmt(self, node: BreakStmt) -> None:
        raise BreakSignal()

    def visit_ContinueStmt(self, node: ContinueStmt) -> None:
        raise ContinueSignal()

    def visit_TryCatchStmt(self, node: TryCatchStmt) -> None:
        try:
            self.execute(node.try_block)
        except (BreakSignal, ContinueSignal, ReturnSignal):
            raise
        except Exception as err:
            if node.catch_block is not None:
                catch_env = Environment(self.environment)
                err_msg = str(err.message if isinstance(err, JLTError) else err)
                if node.error_name:
                    catch_env.define(node.error_name, err_msg)
                if isinstance(node.catch_block, BlockStmt):
                    self.execute_block(node.catch_block.statements, catch_env)
                else:
                    prev = self.environment
                    try:
                        self.environment = catch_env
                        self.execute(node.catch_block)
                    finally:
                        self.environment = prev
            else:
                raise
        finally:
            if node.finally_block is not None:
                self.execute(node.finally_block)

    # =========================================================================
    # Expressions Visitors
    # =========================================================================

    def visit_LiteralExpr(self, node: LiteralExpr) -> Any:
        return node.value

    def visit_VarExpr(self, node: VarExpr) -> Any:
        return self.environment.get(node.name, node.line, node.column, self.source, self.file_path)

    def visit_UnaryExpr(self, node: UnaryExpr) -> Any:
        right = self.evaluate(node.right)
        op = node.op
        if op in ("!", "opposite", "ulta", "not_only", "not"):
            return not self.is_truthy(right)
        elif op == "-":
            if not isinstance(right, (int, float)):
                raise JLTTypeError(
                    f"Minus operator applied to non-number {right!r}!",
                    node.line,
                    node.column,
                    self.source,
                    self.file_path,
                )
            return -right
        elif op == "+":
            return right
        raise JLTRuntimeError(f"Unknown unary operator '{op}'", node.line, node.column, self.source, self.file_path)

    def visit_BinaryExpr(self, node: BinaryExpr) -> Any:
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)
        op = node.op

        # Equality
        if op in ("==", "same_to_same", "ditto"):
            return left == right
        if op in ("!=", "different_only", "not_same"):
            return left != right

        # Arithmetic
        if op == "+":
            if isinstance(left, str) or isinstance(right, str):
                return jlt_format(left) + jlt_format(right)
            if isinstance(left, list) and isinstance(right, list):
                return left + right
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left + right
            raise JLTTypeError(
                f"Cannot add types '{type(left).__name__}' and '{type(right).__name__}'! What macha!",
                node.line,
                node.column,
                self.source,
                self.file_path,
            )

        if op == "-":
            self.check_numeric_operands(op, left, right, node)
            return left - right

        if op == "*":
            if isinstance(left, str) and isinstance(right, int):
                return left * right
            if isinstance(left, list) and isinstance(right, int):
                return left * right
            self.check_numeric_operands(op, left, right, node)
            return left * right

        if op == "/":
            self.check_numeric_operands(op, left, right, node)
            if right == 0:
                raise JLTZeroDivisionError(
                    "Division by zero! Auto meter won't start like that boss!",
                    node.line,
                    node.column,
                    self.source,
                    self.file_path,
                )
            return left / right

        if op == "%":
            self.check_numeric_operands(op, left, right, node)
            if right == 0:
                raise JLTZeroDivisionError(
                    "Modulo by zero! Cannot calculate remainder boss!",
                    node.line,
                    node.column,
                    self.source,
                    self.file_path,
                )
            return left % right

        if op == "^":
            self.check_numeric_operands(op, left, right, node)
            return left ** right

        # Comparison
        if op in (">", "more_than", "jaasti"):
            return left > right
        if op in (">=", "atleast", "jaasti_illa_equal"):
            return left >= right
        if op in ("<", "less_than", "kammi"):
            return left < right
        if op in ("<=", "atmost", "kammi_illa_equal"):
            return left <= right

        raise JLTRuntimeError(f"Unknown binary operator '{op}'", node.line, node.column, self.source, self.file_path)

    def visit_LogicalExpr(self, node: LogicalExpr) -> Any:
        left = self.evaluate(node.left)
        op = node.op

        if op in ("||", "or_else", "athava", "or"):
            if self.is_truthy(left):
                return left
            return self.evaluate(node.right)

        if op in ("&&", "and_also", "matthe", "and"):
            if not self.is_truthy(left):
                return left
            return self.evaluate(node.right)

        raise JLTRuntimeError(f"Unknown logical operator '{op}'", node.line, node.column, self.source, self.file_path)

    def visit_CallExpr(self, node: CallExpr) -> Any:
        callee = self.evaluate(node.callee)
        arguments = [self.evaluate(arg) for arg in node.args]

        if not isinstance(callee, JLTCallable):
            raise JLTTypeError(
                f"What ra! '{callee}' is not a callable function!",
                node.line,
                node.column,
                self.source,
                self.file_path,
            )

        return callee.call(self, arguments, node.line, node.column)

    def visit_ListLiteralExpr(self, node: ListLiteralExpr) -> List[Any]:
        return [self.evaluate(elem) for elem in node.elements]

    def visit_DictLiteralExpr(self, node: DictLiteralExpr) -> Dict[Any, Any]:
        result = {}
        for k_expr, v_expr in node.pairs:
            key = self.evaluate(k_expr)
            val = self.evaluate(v_expr)
            result[key] = val
        return result

    def visit_IndexExpr(self, node: IndexExpr) -> Any:
        target = self.evaluate(node.target)
        index = self.evaluate(node.index)

        try:
            if isinstance(target, (list, tuple, str)):
                idx = int(index)
                return target[idx]
            elif isinstance(target, dict):
                return target.get(index)
            else:
                raise JLTTypeError(
                    f"Cannot index into object of type '{type(target).__name__}'!",
                    node.line,
                    node.column,
                    self.source,
                    self.file_path,
                )
        except IndexError:
            raise JLTRuntimeError(
                f"Index '{index}' out of range! That bus route does not exist boss!",
                node.line,
                node.column,
                self.source,
                self.file_path,
            )

    def visit_MemberExpr(self, node: MemberExpr) -> Any:
        target = self.evaluate(node.target)
        if isinstance(target, dict):
            return target.get(node.property_name)
        raise JLTTypeError(
            f"Cannot access property '{node.property_name}' on non-dict object '{target}'!",
            node.line,
            node.column,
            self.source,
            self.file_path,
        )

    def visit_AssignExpr(self, node: AssignExpr) -> Any:
        val = self.evaluate(node.value)

        if isinstance(node.target, VarExpr):
            if node.op == "+=":
                cur = self.environment.get(node.target.name, node.line, node.column, self.source, self.file_path)
                val = cur + val
            elif node.op == "-=":
                cur = self.environment.get(node.target.name, node.line, node.column, self.source, self.file_path)
                val = cur - val

            self.environment.assign(node.target.name, val, node.line, node.column, self.source, self.file_path)
            return val

        if isinstance(node.target, IndexExpr):
            target_obj = self.evaluate(node.target.target)
            idx = self.evaluate(node.target.index)
            if isinstance(target_obj, list):
                i = int(idx)
                if node.op == "+=":
                    val = target_obj[i] + val
                elif node.op == "-=":
                    val = target_obj[i] - val
                target_obj[i] = val
                return val
            elif isinstance(target_obj, dict):
                if node.op == "+=":
                    val = target_obj.get(idx, 0) + val
                elif node.op == "-=":
                    val = target_obj.get(idx, 0) - val
                target_obj[idx] = val
                return val
            raise JLTTypeError(
                "Cannot assign index on non-collection object!",
                node.line,
                node.column,
                self.source,
                self.file_path,
            )

        if isinstance(node.target, MemberExpr):
            target_obj = self.evaluate(node.target.target)
            if isinstance(target_obj, dict):
                prop = node.target.property_name
                if node.op == "+=":
                    val = target_obj.get(prop, 0) + val
                elif node.op == "-=":
                    val = target_obj.get(prop, 0) - val
                target_obj[prop] = val
                return val
            raise JLTTypeError(
                "Cannot set property on non-dict object!",
                node.line,
                node.column,
                self.source,
                self.file_path,
            )

        raise JLTRuntimeError(f"Invalid assignment target {node.target}", node.line, node.column, self.source, self.file_path)

    # =========================================================================
    # Helpers
    # =========================================================================

    def is_truthy(self, val: Any) -> bool:
        if val is None or val is False:
            return False
        if isinstance(val, (int, float)) and val == 0:
            return False
        if isinstance(val, (str, list, dict)) and len(val) == 0:
            return False
        return True

    def check_numeric_operands(self, op: str, left: Any, right: Any, node: ASTNode) -> None:
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return
        raise JLTTypeError(
            f"Operator '{op}' requires numbers, but got '{type(left).__name__}' and '{type(right).__name__}'! What macha!",
            node.line,
            node.column,
            self.source,
            self.file_path,
        )
