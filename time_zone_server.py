import mcp
from mcp.server.fastmcp import FastMCP
import requests

# 1. Initialize the FastMCP server instance
mcp = FastMCP("Time zone and Currency MCP")

@mcp.tool()
def convert_time_zone(time_zone_source: str, time_zone_target: str, dateTime: str) -> str:
    """Convert a specific date and time from one timezone to another."""
    payload = {
        "dateTime": dateTime,
        "fromTimezone": time_zone_source,
        "toTimezone": time_zone_target
    }
    url = "https://opentimezone.com/convert"
    response = requests.post(url=url, json=payload)
    data = response.json()
    converted_time = data.get("dateTime", "N/A")
    return f"This time {dateTime} in {time_zone_source} to {time_zone_target} is {converted_time}"

@mcp.tool()
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """Convert an amount from one currency to another using exchange rates."""
    url = f"https://api.frankfurter.dev/v1/latest?base={from_currency}&symbols={to_currency}"
    response = requests.get(url)
    data = response.json()
    rate = data['rates'].get(to_currency)

    if rate is None:
        return f"Could not find exchange rate for {from_currency} to {to_currency}"

    converted_amount = amount * rate
    return f"{amount} {from_currency} = {converted_amount:.2f} {to_currency} (Rate: {rate})"

@mcp.resource("file://currencies.txt")
def get_currencies() -> str:
    """Get the list of currency names for conversion."""
    try:
        with open('currencies.txt', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "currencies.txt file not found"

if __name__ == "__main__":
    # Start the server using stdio transport
    mcp.run(transport="stdio")  # standart i/o , http, sse 