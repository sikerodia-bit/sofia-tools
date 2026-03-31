# sofia-tools

A community library of tools for Sofia AI assistant.
Built with security-first design — every tool is
sandboxed and reviewed before inclusion.

## Philosophy
- Security first: all tools declare permissions upfront
- Docker sandboxed: network tools run in isolation
- Caribbean-aware: built for Dominican Republic and
  Haiti context, works everywhere
- Community driven: contribute your own tools

## Available Tools

### Utils
| Tool | Description | Network | Docker |
|------|-------------|---------|--------|
| calculator | Math expressions | No | No |
| datetime | Current time/date | No | No |
| web_search | DuckDuckGo search | Yes | Yes |
| memory | Read/write memory | No | No |
| url_reader | Fetch URL content | Yes | Yes |

### Caribbean
| Tool | Description | Network | Docker |
|------|-------------|---------|--------|
| currency_dop | USD/DOP rates | Yes | No |
| currency_htg | USD/HTG rates | Yes | No |
| weather_caribbean | Caribbean weather | Yes | No |

### Productivity (coming soon)
- gmail, calendar, notion, todoist

### Business (coming soon)
- aws_monitor, stripe, hubspot

### Research (coming soon)
- url_reader, youtube_summary, arxiv

### Communication (coming soon)
- whatsapp, slack, discord

## Installing a Tool

```bash
python install.py calculator
python install.py url_reader
python install.py bundle:utils
python install.py bundle:caribbean
```

## Building Your Own Tool

Copy `tool_template.py` and follow the instructions.
See `docs/building-tools.md` for the full guide.

## Contributing

See `CONTRIBUTING.md` for guidelines.
All PRs welcome — especially Caribbean-specific tools!

## Security Model

| Level | Description |
|-------|-------------|
| 1 | Official tools — reviewed and maintained by core team |
| 2 | Community tools — PR reviewed + automated security scan |
| 3 | Personal tools — local only, no review needed |

## Built by
Dima — CTO, Santo Domingo, Dominican Republic
