# Contributing to sofia-tools

## Getting Started
1. Fork the repository
2. Copy `tool_template.py` to the right category folder
3. Build your tool following the template
4. Add tests in `tests/`
5. Submit a PR

## Tool Requirements
Every tool must:
- Follow `tool_template.py` structure exactly
- Declare all permissions upfront (`requires_network`, `needs_docker`)
- Handle all errors — never raise exceptions to the caller
- Return strings — Sofia sends your output to the AI
- Include a clear description the AI can understand
- Have at least one test

## Security Requirements
- Never hardcode API keys — use environment variables
- Declare `allowed_domains` if `requires_network=True`
- Mark `needs_docker=True` if touching external network
- Never access files outside allowed paths
- Document what data leaves the local machine

## Categories
| Folder | Use for |
|--------|---------|
| `utils/` | General purpose — no specific domain |
| `productivity/` | Gmail, Calendar, Notes, Tasks |
| `business/` | AWS, Stripe, CRM, Analytics |
| `research/` | Web, Documents, Academic papers |
| `caribbean/` | DR, Haiti, Caribbean-specific tools |
| `communication/` | Messaging platforms |

## PR Review Process
1. Automated security scan runs on PR
2. Maintainer reviews tool logic
3. Maintainer reviews permissions declared
4. Tests must pass
5. Merged to main → available to all

## Questions?
Open an issue or discussion on GitHub.
