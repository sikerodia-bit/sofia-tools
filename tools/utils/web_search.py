"""
Web search tool — DuckDuckGo HTML scraper.
- If Docker is available and DOCKER_ENABLED=true → runs in Docker sandbox
- Otherwise → runs directly with httpx (logs security warning)
"""

import logging
import urllib.parse

import httpx
from bs4 import BeautifulSoup

from tools.models import Tool

_log = logging.getLogger("sofia.tools")

TOOL = Tool(
    name="web_search",
    description=(
        "Search the web for current information, news, facts, or any topic. "
        "Use this when the user asks about recent events, wants to look something up, "
        "or asks a question that requires up-to-date information."
    ),
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query to look up.",
            },
            "max_results": {
                "type": "integer",
                "description": "Maximum number of results to return (default 5, max 10).",
                "default": 5,
            },
        },
        "required": ["query"],
    },
    requires_network=True,
    allowed_domains=["html.duckduckgo.com"],
    needs_docker=True,
    timeout_seconds=15,
)

_DDG_HTML_URL = "https://html.duckduckgo.com/html/"

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) "
        "Gecko/20100101 Firefox/120.0"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}


def _parse_ddg_html(html: str, max_results: int) -> list[dict]:
    """Parse DuckDuckGo HTML results page into a list of {title, snippet, url}."""
    soup = BeautifulSoup(html, "html.parser")
    results = []

    for div in soup.find_all("div", class_="result"):
        if len(results) >= max_results:
            break

        classes = div.get("class", [])
        if "result--ad" in classes or "result--more" in classes:
            continue

        title_a = div.find("a", class_="result__a")
        if not title_a:
            continue

        title = title_a.get_text(strip=True)
        if not title:
            continue

        href = title_a.get("href", "")
        parsed_href = urllib.parse.urlparse(href)
        qs = urllib.parse.parse_qs(parsed_href.query)
        if "uddg" in qs:
            real_url = urllib.parse.unquote(qs["uddg"][0])
        elif href.startswith("http"):
            real_url = href
        else:
            real_url = "https://duckduckgo.com" + href

        snippet_tag = div.find("a", class_="result__snippet")
        snippet = snippet_tag.get_text(strip=True) if snippet_tag else ""

        results.append({"title": title, "snippet": snippet, "url": real_url})

    return results


async def run(params: dict) -> str:
    query = params.get("query", "").strip()
    max_results = min(int(params.get("max_results", 5)), 10)

    if not query:
        return "Error: search query is empty."

    _log.warning(
        "WEB_SEARCH_UNSANDBOXED query=%r — Docker unavailable, running direct", query
    )

    try:
        async with httpx.AsyncClient(timeout=12.0, follow_redirects=True) as client:
            resp = await client.get(
                _DDG_HTML_URL,
                params={"q": query},
                headers=_HEADERS,
            )
            resp.raise_for_status()
            html = resp.text
    except httpx.TimeoutException:
        return f"Error: search timed out for query: {query!r}"
    except httpx.HTTPStatusError as e:
        return f"Error: HTTP {e.response.status_code} from DuckDuckGo"
    except Exception as e:
        return f"Error performing search: {str(e)}"

    results = _parse_ddg_html(html, max_results)

    if not results:
        return f"No results found for: {query!r}"

    lines = [f"Search results for: {query!r}\n"]
    for i, r in enumerate(results, 1):
        lines.append(f"{i}. {r['title']}")
        if r["snippet"]:
            lines.append(f"   {r['snippet']}")
        if r["url"]:
            lines.append(f"   {r['url']}")
        lines.append("")
    return "\n".join(lines)
