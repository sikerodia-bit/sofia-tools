"""
Tests for tools/utils/calculator.py
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.utils.calculator import safe_eval, run


# ── safe_eval unit tests ──────────────────────────────────────────────────────

def test_addition():
    assert safe_eval("2 + 2") == 4.0

def test_subtraction():
    assert safe_eval("10 - 3") == 7.0

def test_multiplication():
    assert safe_eval("6 * 7") == 42.0

def test_division():
    assert safe_eval("10 / 4") == 2.5

def test_power():
    assert safe_eval("2 ** 10") == 1024.0

def test_modulo():
    assert safe_eval("17 % 5") == 2.0

def test_floor_div():
    assert safe_eval("17 // 5") == 3.0

def test_sqrt():
    assert safe_eval("sqrt(144)") == 12.0

def test_nested():
    assert safe_eval("(47.50 * 1.15)") == pytest.approx(54.625)

def test_percentage():
    assert safe_eval("15 * 0.15") == pytest.approx(2.25)

def test_division_by_zero():
    with pytest.raises(ValueError, match="Division by zero"):
        safe_eval("1 / 0")

def test_disallowed_operator():
    with pytest.raises(ValueError):
        safe_eval("__import__('os')")

def test_string_literal():
    with pytest.raises(ValueError):
        safe_eval("'hello'")

def test_unknown_function():
    with pytest.raises(ValueError, match="Unknown function"):
        safe_eval("open('file.txt')")


# ── run() integration tests ───────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_run_basic():
    result = await run({"expression": "2 + 2"})
    assert result == "2 + 2 = 4"

@pytest.mark.asyncio
async def test_run_empty():
    result = await run({"expression": ""})
    assert "Error" in result

@pytest.mark.asyncio
async def test_run_missing_param():
    result = await run({})
    assert "Error" in result

@pytest.mark.asyncio
async def test_run_formats_integer():
    result = await run({"expression": "100 / 4"})
    assert result == "100 / 4 = 25"

@pytest.mark.asyncio
async def test_run_formats_float():
    result = await run({"expression": "1 / 3"})
    assert "0.333" in result
