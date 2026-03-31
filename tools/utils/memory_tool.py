"""
Memory tool — read/write Sofia's persistent memory.
Runs directly (needs access to ~/.sofia/) but with strict path validation.
Path traversal attacks are blocked at every layer.
"""

import json
import re
from pathlib import Path

from tools.models import Tool

TOOL = Tool(
    name="memory",
    description=(
        "Read or write a persistent memory entry. Use 'read' to recall a fact "
        "Sofia has stored, 'write' to save new information for future sessions. "
        "Keys should be short snake_case identifiers like 'user_preference_language'."
    ),
    parameters={
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["read", "write", "list"],
                "description": "Operation to perform: read, write, or list all keys.",
            },
            "key": {
                "type": "string",
                "description": "Memory key (alphanumeric + underscores, max 64 chars).",
            },
            "value": {
                "type": "string",
                "description": "Value to write (required for 'write' operation).",
            },
        },
        "required": ["operation"],
    },
    requires_network=False,
    needs_docker=False,
    timeout_seconds=5,
)

# Only alphanumeric + underscores — no path components
_KEY_RE = re.compile(r"^[a-zA-Z0-9_]{1,64}$")


def _workspace() -> Path:
    """Return the writable workspace directory, creating it if needed."""
    ws = Path.home() / ".sofia" / "workspace"
    ws.mkdir(parents=True, exist_ok=True)
    return ws


def _validate_key(key: str) -> str:
    """Raise ValueError if key is unsafe, else return it."""
    if not _KEY_RE.match(key):
        raise ValueError(
            f"Invalid key {key!r}. Keys must be alphanumeric + underscores, max 64 chars."
        )
    return key


async def run(params: dict) -> str:
    operation = params.get("operation", "").lower()
    key = params.get("key", "").strip()
    value = params.get("value", "")

    workspace = _workspace()

    if operation == "list":
        keys = [f.stem for f in workspace.glob("*.json")]
        if not keys:
            return "No memory entries stored yet."
        return "Stored memory keys:\n" + "\n".join(f"  - {k}" for k in sorted(keys))

    if operation == "read":
        try:
            _validate_key(key)
        except ValueError as exc:
            return str(exc)
        path = workspace / f"{key}.json"
        if not path.exists():
            return f"No memory entry found for key: {key!r}"
        data = json.loads(path.read_text())
        return f"{key}: {data['value']}"

    if operation == "write":
        try:
            _validate_key(key)
        except ValueError as exc:
            return str(exc)
        if not value:
            return "Error: 'value' is required for write operation."
        path = workspace / f"{key}.json"
        if not path.resolve().is_relative_to(workspace.resolve()):
            return "Error: path traversal detected."
        path.write_text(json.dumps({"key": key, "value": value}))
        return f"Saved: {key} = {value!r}"

    return f"Unknown operation: {operation!r}. Use 'read', 'write', or 'list'."
