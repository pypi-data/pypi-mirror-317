import re
from typing import Optional, Dict
import aiohttp
from numo.domain.interfaces.numo_module import NumoModule
import time


class CurrencyModule(NumoModule):
    """
    Currency conversion module.
    Provides real-time currency conversion using external exchange rate API.
    Includes caching mechanism to optimize API usage.
    """

    def __init__(self):
        """Initialize with currency pattern and API settings."""
        self._pattern = r"^(\d+(?:\.\d+)?)\s*([A-Za-z]{3})\s*to\s*([A-Za-z]{3})$"
        self._api_url = "https://api.exchangerate-api.com/v4/latest/USD"
        self._rates: Dict[str, float] = {}
        self._last_update = 0
        self._cache_duration = 24 * 60 * 60  # 24 hours in seconds

    async def run(self, source: str) -> Optional[str]:
        """
        Convert amount between currencies.

        Args:
            source: Input in format: [amount] [from_currency] to [to_currency]

        Returns:
            str: Converted amount if successful
            None: For any error or invalid input

        Example:
            >>> module = CurrencyModule()
            >>> await module.run("100 USD to EUR")  # Returns "85.23 EUR"
            >>> await module.run("invalid")  # Returns None
        """
        if not source or not isinstance(source, str):
            return None

        # Parse conversion request
        match = re.match(self._pattern, source, re.IGNORECASE)
        if not match:
            return None

        try:
            amount = float(match.group(1))
            from_curr = match.group(2).upper()
            to_curr = match.group(3).upper()
        except (ValueError, TypeError):
            return None

        # Get exchange rates
        rates = await self._get_exchange_rates()
        if not rates:
            return None

        # Validate currencies
        if from_curr not in rates or to_curr not in rates:
            return None

        try:
            # Convert amount
            result = amount * (rates[to_curr] / rates[from_curr])
            return self._format_result(result, to_curr)
        except (ValueError, ZeroDivisionError):
            return None

    async def _get_exchange_rates(self) -> Optional[Dict[str, float]]:
        """
        Fetch current exchange rates from API.
        Uses cached rates if they are still valid.

        Returns:
            dict: Exchange rates if successful
            None: For any error
        """
        current_time = time.time()

        # Use cached data if still valid
        if self._rates and (current_time - self._last_update) < self._cache_duration:
            return self._rates

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self._api_url) as response:
                    if response.status != 200:
                        return self._rates if self._rates else None

                    data = await response.json()
                    if not data or "rates" not in data:
                        return self._rates if self._rates else None

                    rates = data["rates"]
                    if not isinstance(rates, dict):
                        return self._rates if self._rates else None

                    # Add base currency
                    rates["USD"] = 1.0

                    # Update cache
                    self._rates = rates
                    self._last_update = current_time
                    return rates

        except (aiohttp.ClientError, ValueError, KeyError):
            # Return cached rates if available, otherwise None
            return self._rates if self._rates else None

    def _format_result(self, value: float, currency: str) -> str:
        """Format currency amount with 2 decimal places and currency code."""
        try:
            return f"{value:.2f} {currency}"
        except (ValueError, TypeError):
            return str(value)
