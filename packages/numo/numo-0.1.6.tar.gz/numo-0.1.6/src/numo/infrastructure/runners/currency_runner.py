import re
from typing import Optional, Dict
import aiohttp
from numo.domain.interfaces.numo_runner import NumoRunner


class CurrencyRunner(NumoRunner):
    """
    Runner for converting between different currencies.
    Uses external exchange rate API for conversions.
    Never raises exceptions - returns None for any error condition.
    """

    def __init__(self):
        """Initialize with currency pattern and API settings."""
        self._pattern = r"^(\d+(?:\.\d+)?)\s*([A-Za-z]{3})\s*to\s*([A-Za-z]{3})$"
        self._api_url = "https://api.exchangerate-api.com/v4/latest/USD"
        self._rates: Dict[str, float] = {}
        self._last_update = 0

    async def run(self, source: str) -> Optional[str]:
        """
        Convert amount between currencies.

        Args:
            source: Input in format: [amount] [from_currency] to [to_currency]

        Returns:
            str: Converted amount if successful
            None: For any error or invalid input

        Example:
            >>> runner = CurrencyRunner()
            >>> await runner.run("100 USD to EUR")  # Returns "85.23 EUR"
            >>> await runner.run("invalid")  # Returns None
        """
        if not source or not isinstance(source, str):
            return None

        try:
            # Parse conversion request
            match = re.match(self._pattern, source, re.IGNORECASE)
            if not match:
                return None

            amount = float(match.group(1))
            from_curr = match.group(2).upper()
            to_curr = match.group(3).upper()

            # Get exchange rates
            rates = await self._get_exchange_rates()
            if not rates:
                return None

            # Validate currencies
            if from_curr not in rates or to_curr not in rates:
                return None

            # Convert amount
            result = amount * (rates[to_curr] / rates[from_curr])
            return self._format_result(result, to_curr)

        except:  # Catch absolutely everything
            return None

    async def _get_exchange_rates(self) -> Optional[Dict[str, float]]:
        """
        Fetch current exchange rates from API.

        Returns:
            dict: Exchange rates if successful
            None: For any error
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self._api_url) as response:
                    if response.status != 200:
                        return None

                    data = await response.json()
                    if not data or "rates" not in data:
                        return None

                    rates = data["rates"]
                    if not isinstance(rates, dict):
                        return None

                    # Add base currency
                    rates["USD"] = 1.0
                    return rates

        except:  # Catch absolutely everything
            return None

    def _format_result(self, value: float, currency: str) -> str:
        """Format currency amount with 2 decimal places and currency code."""
        try:
            return f"{value:.2f} {currency}"
        except:
            return str(value)
