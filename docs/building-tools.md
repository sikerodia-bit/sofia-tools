# Building Tools for Sofia

## Quick Start

```bash
# 1. Copy the template
cp tool_template.py tools/utils/my_tool.py

# 2. Edit it — fill in metadata and write your function
# 3. Test it
pytest tests/test_my_tool.py

# 4. Install into Sofia
python install.py my_tool
```

## The Golden Rules

1. **Always return a string** — Sofia sends your output directly to the AI
2. **Never raise exceptions** — catch everything, return an error string
3. **Declare permissions honestly** — `requires_network`, `needs_docker`, `allowed_domains`
4. **Keep descriptions clear** — the AI reads `description` to decide when to call your tool
5. **Handle timeouts gracefully** — network calls can hang; always set a timeout

## Tool Structure

Every tool has two parts:

### 1. The `TOOL` metadata object

```python
from tools.models import Tool

TOOL = Tool(
    name="my_tool",               # snake_case, must be unique in Sofia
    description="...",            # AI reads this to decide when to use the tool
    parameters={...},             # JSON Schema
    requires_network=False,
    allowed_domains=[],
    needs_docker=False,
    timeout_seconds=10,
)
```

### 2. The `run()` function

```python
async def run(params: dict) -> str:
    value = params.get("my_param", "")
    try:
        # do the work
        return f"Result: {value}"
    except Exception as e:
        return f"Error: {str(e)}"
```

Sofia calls `run(params)` — `params` is always a dict with the tool's parameters.

## Writing Good Descriptions

The AI uses `description` to decide when to call your tool.
Be specific about:
- When to use it (triggers)
- What it returns
- Example queries that should trigger it

```python
# Bad — too vague
description="Gets weather information"

# Good — specific triggers + return format
description=(
    "Get current weather conditions for any city. "
    "Use when user asks about weather, temperature, or forecast. "
    "Example: 'What's the weather in Santo Domingo?' "
    "Returns: temperature, conditions, humidity, wind."
)
```

## Tool Categories

| Folder | Use for |
|--------|---------|
| `utils/` | Works everywhere, no specific domain |
| `productivity/` | Email, calendar, tasks, notes |
| `business/` | AWS, payments, CRM, analytics |
| `research/` | Web, documents, academic papers |
| `caribbean/` | DR, Haiti, Caribbean-specific tools |
| `communication/` | Messaging platforms |

## Security Guidelines

### Permissions you must declare

| Field | When to set True |
|-------|-----------------|
| `requires_network` | Tool makes any HTTP/network call |
| `needs_docker` | Tool fetches user-supplied URLs or runs untrusted content |

### Never do this
- Hardcode API keys — use `os.environ.get("MY_API_KEY")`
- Access files outside allowed paths
- Call `eval()` or `exec()` with user input
- Skip timeout on network calls

### Always do this
- List `allowed_domains` when `requires_network=True`
- Set `needs_docker=True` when fetching arbitrary user-supplied URLs
- Document what data leaves the local machine

## Registering in Sofia

After installing (`python install.py my_tool`), add to `sofia/tools/registry.py`:

```python
from tools.builtin.my_tool import TOOL as MY_TOOL, run as my_tool_run

TOOLS = {
    # existing tools...
    "my_tool": (MY_TOOL, my_tool_run),
}
```

## Testing Your Tool

```python
# tests/test_my_tool.py
import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.utils.my_tool import run, TOOL

def test_tool_metadata():
    assert TOOL.name == "my_tool"
    assert TOOL.requires_network is False

@pytest.mark.asyncio
async def test_basic():
    result = await run({"my_param": "hello"})
    assert "Result" in result

@pytest.mark.asyncio
async def test_empty_input():
    result = await run({})
    assert isinstance(result, str)  # never raises
```

Run with: `pytest tests/ -v`

## Submitting a PR

1. Fork the repo
2. Build and test your tool
3. `git add tools/category/my_tool.py tests/test_my_tool.py`
4. Submit PR with:
   - What the tool does
   - What API/service it calls (if any)
   - Any API keys required
