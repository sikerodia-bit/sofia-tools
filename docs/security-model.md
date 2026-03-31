# Security Model

## Trust Levels

### Level 1 — Official Tools
- Maintained by the core team
- Full code review before inclusion
- Automated security scanning on every commit
- Examples: `calculator`, `datetime_tool`, `memory_tool`

### Level 2 — Community Tools
- Submitted via PR
- Automated security scan (bandit, semgrep)
- Manual review by maintainer
- Must pass all tests before merge
- Examples: any PR-merged tool

### Level 3 — Personal Tools
- Local only, never submitted to this repo
- No review required
- Use `tool_template.py` as a starting point
- Register directly in your Sofia instance

## Permission System

Every tool declares its permissions upfront in the `Tool` metadata:

```python
Tool(
    requires_network=False,   # Does it make HTTP calls?
    allowed_domains=[],       # Which domains? (empty = no network)
    needs_docker=False,       # Run in Docker sandbox?
    timeout_seconds=10,       # Max execution time
)
```

### `requires_network`
Set to `True` if the tool makes any network call.
When `True`, you must also populate `allowed_domains`.

### `allowed_domains`
Explicit list of domains the tool is allowed to contact.
Sofia's executor can enforce this to prevent unexpected outbound calls.
Set to `[]` (empty) only for tools like `url_reader` that intentionally
fetch arbitrary user-supplied URLs — and set `needs_docker=True` in that case.

### `needs_docker`
Set to `True` when:
- The tool fetches content from arbitrary/user-supplied URLs
- The tool runs code from external sources
- You want network isolation for any other reason

Docker sandbox prevents the tool from accessing your local filesystem
or internal network even if the fetched content is malicious.

### `timeout_seconds`
All tools have a hard timeout enforced by Sofia's executor.
- Local tools: 5-10 seconds
- Network tools: 15-30 seconds

## What Leaves Your Machine

Each tool's `allowed_domains` tells you exactly what external services
are contacted. Review this before installing any tool.

| Tool | Data sent externally |
|------|---------------------|
| calculator | Nothing — pure local |
| datetime_tool | Nothing — pure local |
| memory_tool | Nothing — local filesystem |
| web_search | Your search query → DuckDuckGo |
| url_reader | The URL you provide → that website |
| currency_dop | Nothing with PII → open.er-api.com |
| currency_htg | Nothing with PII → open.er-api.com |

## Reporting Security Issues

Open a GitHub issue marked `[SECURITY]`.
For sensitive issues, contact the maintainer directly.
