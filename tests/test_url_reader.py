"""
Tests for tools/utils/url_reader.py
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.utils.url_reader import run, TOOL


# ── Metadata tests ────────────────────────────────────────────────────────────

def test_tool_metadata():
    assert TOOL.name == "url_reader"
    assert TOOL.requires_network is True
    assert TOOL.needs_docker is True
    assert TOOL.timeout_seconds == 15

def test_tool_has_url_param():
    props = TOOL.parameters["properties"]
    assert "url" in props
    assert "url" in TOOL.parameters["required"]


# ── Validation tests ──────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_missing_url():
    result = await run({})
    assert "Error" in result

@pytest.mark.asyncio
async def test_invalid_url_scheme():
    result = await run({"url": "ftp://example.com"})
    assert "Error" in result
    assert "https://" in result

@pytest.mark.asyncio
async def test_empty_url():
    result = await run({"url": ""})
    assert "Error" in result


# ── HTTP success mock ─────────────────────────────────────────────────────────

SAMPLE_HTML = """
<html>
<head><title>Test Page</title></head>
<body>
  <nav>Navigation stuff</nav>
  <h1>Hello World</h1>
  <p>This is the main content.</p>
  <script>alert('ignored')</script>
  <footer>Footer stuff</footer>
</body>
</html>
"""


@pytest.mark.asyncio
async def test_successful_fetch():
    mock_response = MagicMock()
    mock_response.text = SAMPLE_HTML
    mock_response.raise_for_status = MagicMock()

    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.get = AsyncMock(return_value=mock_response)

    with patch("tools.utils.url_reader.httpx.AsyncClient", return_value=mock_client):
        result = await run({"url": "https://example.com"})

    assert "Test Page" in result
    assert "Hello World" in result
    assert "main content" in result
    # boilerplate should be stripped
    assert "Navigation stuff" not in result
    assert "Footer stuff" not in result
    assert "alert" not in result


@pytest.mark.asyncio
async def test_truncation():
    long_content = "word " * 2000  # ~10000 chars
    html = f"<html><head><title>Long</title></head><body><p>{long_content}</p></body></html>"

    mock_response = MagicMock()
    mock_response.text = html
    mock_response.raise_for_status = MagicMock()

    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.get = AsyncMock(return_value=mock_response)

    with patch("tools.utils.url_reader.httpx.AsyncClient", return_value=mock_client):
        result = await run({"url": "https://example.com", "max_chars": 500})

    assert "Truncated" in result


# ── HTTP error mocks ──────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_timeout_error():
    import httpx

    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.get = AsyncMock(side_effect=httpx.TimeoutException("timeout"))

    with patch("tools.utils.url_reader.httpx.AsyncClient", return_value=mock_client):
        result = await run({"url": "https://example.com"})

    assert "timed out" in result.lower()


@pytest.mark.asyncio
async def test_http_404():
    import httpx

    mock_response = MagicMock()
    mock_response.status_code = 404
    error = httpx.HTTPStatusError("404", request=MagicMock(), response=mock_response)

    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.get = AsyncMock(side_effect=error)

    with patch("tools.utils.url_reader.httpx.AsyncClient", return_value=mock_client):
        result = await run({"url": "https://example.com/notfound"})

    assert "404" in result
