"""
Tests for tools/utils/datetime_tool.py
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.utils.datetime_tool import run


@pytest.mark.asyncio
async def test_default_timezone():
    result = await run({})
    assert "America/Santo_Domingo" in result
    assert "Date:" in result
    assert "Time:" in result

@pytest.mark.asyncio
async def test_utc_timezone():
    result = await run({"timezone": "UTC"})
    assert "UTC" in result

@pytest.mark.asyncio
async def test_new_york_timezone():
    result = await run({"timezone": "America/New_York"})
    assert "America/New_York" in result

@pytest.mark.asyncio
async def test_invalid_timezone_fallback():
    result = await run({"timezone": "Fake/Timezone"})
    assert "fallback" in result
    assert "America/Santo_Domingo" in result

@pytest.mark.asyncio
async def test_target_date_future():
    result = await run({"target_date": "2099-01-01"})
    assert "days" in result

@pytest.mark.asyncio
async def test_target_date_past():
    result = await run({"target_date": "2000-01-01"})
    assert "ago" in result or "days" in result

@pytest.mark.asyncio
async def test_invalid_target_date():
    result = await run({"target_date": "not-a-date"})
    assert "Could not parse" in result

@pytest.mark.asyncio
async def test_returns_string():
    result = await run({})
    assert isinstance(result, str)
    assert len(result) > 0
