# Getting Started with sofia-tools

## Prerequisites
- Sofia installed at `C:/xampp/htdocs/sofia`
- Python 3.11+
- pip packages: `httpx`, `beautifulsoup4`

## Install a Tool

```bash
cd C:/xampp/htdocs/sofia-tools

# Install a single tool
python install.py calculator
python install.py url_reader

# Install a whole bundle
python install.py bundle:utils
python install.py bundle:caribbean

# See what's available
python install.py list
```

## Activate in Sofia

After installing, add the tool to Sofia's registry:

```python
# sofia/tools/registry.py

from tools.builtin.url_reader import TOOL as URL_READER_TOOL, run as url_reader_run

TOOLS = {
    # ... existing tools ...
    "url_reader": (URL_READER_TOOL, url_reader_run),
}
```

Then restart Sofia — the tool is active.

## Test a Tool

```bash
cd C:/xampp/htdocs/sofia-tools
pip install pytest pytest-asyncio
pytest tests/
```
