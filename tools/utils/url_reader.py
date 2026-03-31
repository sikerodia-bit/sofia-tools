"""
URL Reader Tool
Fetches a URL and returns clean readable text.
Runs in Docker for security isolation.
"""

import httpx
from bs4 import BeautifulSoup

from tools.models import Tool

TOOL = Tool(
    name="url_reader",
    description=(
        "Fetch and read the content of any URL. "
        "Use this when the user asks you to: read a specific webpage or article, "
        "summarize content from a URL, check what a website says, or read documentation at a link. "
        "Example: 'Read https://example.com and summarize it'. "
        "Returns: Clean text content from the page."
    ),
    parameters={
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "description": "Full URL to fetch including https://",
            },
            "max_chars": {
                "type": "integer",
                "description": "Max characters to return (default 3000)",
                "default": 3000,
            },
        },
        "required": ["url"],
    },
    requires_network=True,
    allowed_domains=[],         # empty = allow any domain
    needs_docker=True,
    timeout_seconds=15,
)

_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; Sofia/1.0)",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "en-US,en;q=0.9",
}


async def run(params: dict) -> str:
    url = params.get("url", "").strip()
    max_chars = int(params.get("max_chars", 3000))

    if not url:
        return "Error: url is required."

    if not url.startswith(("http://", "https://")):
        return "Error: URL must start with http:// or https://"

    try:
        async with httpx.AsyncClient(
            timeout=12.0,
            follow_redirects=True,
        ) as client:
            response = await client.get(url, headers=_HEADERS)
            response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove boilerplate elements
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        text = soup.get_text(separator="\n", strip=True)

        lines = [line.strip() for line in text.splitlines() if line.strip()]
        clean_text = "\n".join(lines)

        if len(clean_text) > max_chars:
            clean_text = (
                clean_text[:max_chars]
                + f"\n\n[Truncated — {len(clean_text)} total chars]"
            )

        title = soup.find("title")
        title_text = title.get_text().strip() if title else url

        return f"Page: {title_text}\nURL: {url}\n\n{clean_text}"

    except httpx.TimeoutException:
        return f"Error: Request timed out fetching {url}"
    except httpx.HTTPStatusError as e:
        return f"Error: HTTP {e.response.status_code} from {url}"
    except Exception as e:
        return f"Error reading {url}: {str(e)}"
