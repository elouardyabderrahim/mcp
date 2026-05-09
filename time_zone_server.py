import mcp
from  mcp.server.fastmcp import FastMCP
import requests

mcp = FastMCP("Time zone  and Currency MCP")

@mcp.tool()
def convert_time_zone(time_zone_source: str ,time_zone_target : str,dateTime: str   ) -> str :
    
    payload = {
    "dateTime": dateTime,
    "fromTimezone": time_zone_source,
    "toTimezone": time_zone_target
        }
    
    url="https://opentimezone.com/convert"
    response = requests.post(url=url,json=payload)

    data=response.json()
    converted_time = data.get("dateTime","N/A")
    return  f" this time {dateTime} in {time_zone_source} to {time_zone_target} is {converted_time}"

@mcp.tool()
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    # Complete the docstring with the function arguments
    """
    Convert an amount from one currency to another using current exchange rates.

    Args:
        amount: The amount to convert
        from_currency: Source currency code (e.g., 'USD', 'EUR', 'GBP')
        to_currency: Target currency code (e.g., 'USD', 'EUR', 'GBP')

    Returns:
        A string with the conversion result and exchange rate
    """

    url = f"https://api.frankfurter.dev/v1/latest?base={from_currency}&symbols={to_currency}"

    response = requests.get(url)
    data = response.json()
    rate = data['rates'].get(to_currency)

    if rate is None:
        return f"Could not find exchange rate for {from_currency} to {to_currency}"

    converted_amount = amount * rate
    return f"{amount} {from_currency} = {converted_amount:.2f} {to_currency} (Rate: {rate})"

print(convert_currency(amount=100, from_currency="EUR", to_currency="USD"))


if __name__ == "__main__":
    mcp.run(transport="stdio") # standart i/o , http, sse 