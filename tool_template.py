"""
Sofia Tool Template
═══════════════════
Copy this file to the right category folder.
Rename it to your_tool_name.py
Follow all the instructions in the comments.

Quick checklist:
□ Tool metadata filled in (name, description, parameters)
□ Permissions declared honestly (network, docker, domains)
□ run() is async and returns a string
□ All errors caught — never raises exceptions
□ Added to tools/registry.py in Sofia
□ Test written in tests/
"""

from tools.models import Tool

# ═══════════════════════════════════════════════════
# STEP 1: Tool Metadata
# The AI reads 'description' to decide when to use
# this tool. Make it specific and clear.
# ═══════════════════════════════════════════════════

TOOL = Tool(
    name="your_tool_name",          # snake_case, unique
    description=(
        "[REQUIRED] Clear description of what this tool does. "
        "Use this when: [specific triggers]. "
        "Example queries: '[example question that should trigger this]'. "
        "Returns: [what the output looks like]."
    ),
    parameters={
        "type": "object",
        "properties": {
            "param1": {
                "type": "string",
                "description": "Clear description of this param"
            },
            # Add more parameters as needed
            # Supported types: string, integer, number, boolean
        },
        "required": ["param1"]      # only truly required params
    },

    # ── Permissions ──────────────────────────────────
    # Be honest about these — they affect security

    requires_network=False,         # Does it call external APIs?

    allowed_domains=[               # If network=True, list ALL
        # "api.example.com",        # domains this tool calls.
        # "www.example.com",        # Leave empty if no network.
    ],

    needs_docker=False,             # True → run in Docker sandbox
                                    # Required when requires_network=True
                                    # and tool runs untrusted content

    timeout_seconds=10,             # Max execution time
                                    # Network tools: 15-30s
                                    # Local tools: 5-10s
)

# ═══════════════════════════════════════════════════
# STEP 2: Tool Function
# Must be async. Must return a string.
# Sofia calls run(params) — params is a dict.
# The string goes back to the AI as context.
# Handle ALL errors — Sofia must never crash.
# ═══════════════════════════════════════════════════

async def run(params: dict) -> str:
    """
    Entry point called by Sofia's executor.
    Extract your parameters from the params dict.
    Always return a string.
    """
    param1 = params.get("param1", "").strip()

    if not param1:
        return "Error: param1 is required."

    try:
        # Your implementation here
        result = f"Result for {param1}"
        return result

    except Exception as e:
        # Always return a string, never raise.
        # Sofia will pass this error message to the AI.
        return f"Tool error: {str(e)}"

# ═══════════════════════════════════════════════════
# STEP 3: Register in Sofia
# Add these lines to sofia/tools/registry.py:
#
# from tools.builtin.your_tool_name import TOOL, run
#
# Then add to TOOLS dict:
# "your_tool_name": (TOOL, run),
# ═══════════════════════════════════════════════════
