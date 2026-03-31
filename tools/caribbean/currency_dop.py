"""
Dominican Peso Exchange Rate Tool
Gets current USD/DOP exchange rate.
Free API — no key required.
"""

import httpx

from tools.models import Tool

TOOL = Tool(
    name="currency_dop",
    description=(
        "Get current Dominican Peso (DOP) exchange rates. "
        "Use when user asks about: USD to DOP conversion, DOP to USD conversion, "
        "current peso exchange rate, or how much is X dollars in pesos. "
        "Example: 'How much is $500 in Dominican pesos?' "
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
                "description": "Source currency: USD or DOP",
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

        usd_to_dop = data["rates"]["DOP"]
        updated = data.get("time_last_update_utc", "recently")

        if from_currency == "USD":
            converted = amount * usd_to_dop
            return (
                f"Exchange Rate: 1 USD = {usd_to_dop:.2f} DOP\n"
                f"{amount:g} USD = {converted:.2f} DOP\n"
                f"Rate updated: {updated}"
            )
        elif from_currency == "DOP":
            converted = amount / usd_to_dop
            return (
                f"Exchange Rate: 1 USD = {usd_to_dop:.2f} DOP\n"
                f"{amount:g} DOP = {converted:.4f} USD\n"
                f"Rate updated: {updated}"
            )
        else:
            return f"Unsupported currency: {from_currency}. Use USD or DOP."

    except httpx.TimeoutException:
        return "Error: Request timed out fetching DOP exchange rate."
    except httpx.HTTPStatusError as e:
        return f"Error: HTTP {e.response.status_code} from exchange rate API."
    except Exception as e:
        return f"Error fetching DOP exchange rate: {str(e)}"
