"""
Calculator tool — pure Python, no Docker needed.
Uses AST parsing so eval() is never called directly.
Only allows arithmetic, math functions, and numeric literals.
"""

import ast
import math
import operator
from typing import Any

from tools.models import Tool

TOOL = Tool(
    name="calculate",
    description=(
        "Evaluate a mathematical expression. Use for arithmetic, percentages, "
        "currency conversions, tips, unit conversions, or any numeric calculation. "
        "Supports +, -, *, /, **, %, sqrt, log, sin, cos, tan, floor, ceil, abs, round."
    ),
    parameters={
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": (
                    "A mathematical expression to evaluate. "
                    "Examples: '15 * 0.15', 'sqrt(144)', '(47.50 * 1.15)'."
                ),
            }
        },
        "required": ["expression"],
    },
    requires_network=False,
    needs_docker=False,
    timeout_seconds=5,
)

# Whitelisted binary operators
_BINOPS: dict[type, Any] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
}

# Whitelisted unary operators
_UNOPS: dict[type, Any] = {
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

# Whitelisted math functions (from stdlib math module)
_MATH_FUNCS = {
    name: getattr(math, name)
    for name in [
        "sqrt", "log", "log2", "log10", "exp",
        "sin", "cos", "tan", "asin", "acos", "atan", "atan2",
        "floor", "ceil", "factorial",
        "degrees", "radians", "hypot",
    ]
}
_MATH_FUNCS["abs"] = abs
_MATH_FUNCS["round"] = round


def _eval_node(node: ast.AST) -> float:
    """Recursively evaluate a whitelisted AST node."""
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return float(node.value)
        raise ValueError(f"Non-numeric constant: {node.value!r}")

    if isinstance(node, ast.BinOp):
        op_fn = _BINOPS.get(type(node.op))
        if op_fn is None:
            raise ValueError(f"Disallowed operator: {type(node.op).__name__}")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        if isinstance(node.op, ast.Div) and right == 0:
            raise ValueError("Division by zero")
        return op_fn(left, right)

    if isinstance(node, ast.UnaryOp):
        op_fn = _UNOPS.get(type(node.op))
        if op_fn is None:
            raise ValueError(f"Disallowed unary operator: {type(node.op).__name__}")
        return op_fn(_eval_node(node.operand))

    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only simple function names allowed")
        fn = _MATH_FUNCS.get(node.func.id)
        if fn is None:
            raise ValueError(f"Unknown function: {node.func.id!r}")
        args = [_eval_node(a) for a in node.args]
        return fn(*args)

    raise ValueError(f"Unsupported expression type: {type(node).__name__}")


def safe_eval(expression: str) -> float:
    """Parse and evaluate a math expression without using eval()."""
    try:
        tree = ast.parse(expression.strip(), mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression syntax: {exc}") from exc
    return _eval_node(tree.body)


async def run(params: dict) -> str:
    expression = params.get("expression", "").strip()
    if not expression:
        return "Error: no expression provided."

    try:
        result = safe_eval(expression)
        if result == int(result) and abs(result) < 1e15:
            formatted = str(int(result))
        else:
            formatted = f"{result:,.6f}".rstrip("0").rstrip(".")
        return f"{expression} = {formatted}"
    except (ValueError, ZeroDivisionError, OverflowError) as exc:
        return f"Calculation error: {exc}"
