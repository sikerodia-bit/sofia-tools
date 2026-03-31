"""
Tool data models — mirrors sofia/tools/models.py.
Shared across all tools in this library.
"""

from dataclasses import dataclass, field


@dataclass
class Tool:
    name: str
    description: str
    parameters: dict          # JSON Schema for the tool's input parameters
    requires_network: bool = False
    allowed_domains: list[str] = field(default_factory=list)
    timeout_seconds: int = 10
    needs_docker: bool = False  # True → run in Docker sandbox; False → run directly

    def to_openai_schema(self) -> dict:
        """OpenAI / DeepSeek function-calling format."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }

    def to_anthropic_schema(self) -> dict:
        """Anthropic tool_use format."""
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.parameters,
        }
