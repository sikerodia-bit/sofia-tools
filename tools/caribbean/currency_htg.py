"""
Haitian Gourde Exchange Rate Tool
Gets current USD/HTG exchange rate.
Free API — no key required.
"""

import httpx

from tools.models import Tool

TOOL = Tool(
    name="currency_htg",
    description=(
        "Get current Haitian Gourde (HTG) exchange rates. "
        "Use when user asks about: USD to HTG conversion, HTG to USD conversion, "
        "current gourde exchange rate, or how much is X dollars in gourdes. "
        "Example: 'How much is $100 in Haitian gourdes?' "
        "Returns: Current exchange rate and converted amount."
    ),
    parameters={
        "type": "object",
        "properties": {
            "amount": {
                "type": "number",
                "description": "Amount to convert",
                "default": 1,
            },
            "from_currency": {
                "type": "string",
                "description": "Source currency: USD or HTG",
                "default": "USD",
            },
        },
        "required": [],
    },
    requires_network=True,
    allowed_domains=["open.er-api.com"],
    needs_docker=False,
    timeout_seconds=10,
)

_RATES_URL = "https://open.er-api.com/v6/latest/USD"


async def run(params: dict) -> str:
    amount = float(params.get("amount", 1))
    from_currency = params.get("from_currency", "USD").upper().strip()

    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            response = await client.get(_RATES_URL)
            response.raise_for_status()
            data = response.json()

        usd_to_htg = data["rates"]["HTG"]
        updated = data.get("time_last_update_utc", "recently")

        if from_currency == "USD":
            converted = amount * usd_to_htg
            return (
                f"Exchange Rate: 1 USD = {usd_to_htg:.2f} HTG\n"
                f"{amount:g} USD = {converted:.2f} HTG\n"
                f"Rate updated: {updated}"
            )
        elif from_currency == "HTG":
            converted = amount / usd_to_htg
            return (
                f"Exchange Rate: 1 USD = {usd_to_htg:.2f} HTG\n"
                f"{amount:g} HTG = {converted:.4f} USD\n"
                f"Rate updated: {updated}"
            )
        else:
            return f"Unsupported currency: {from_currency}. Use USD or HTG."

    except httpx.TimeoutException:
        return "Error: Request timed out fetching HTG exchange rate."
    except httpx.HTTPStatusError as e:
        return f"Error: HTTP {e.response.status_code} from exchange rate API."
    except Exception as e:
        return f"Error fetching HTG exchange rate: {str(e)}"
