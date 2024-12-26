import re
from datetime import datetime, timedelta
from typing import Dict, Optional
import aiohttp
from numo.domain.interfaces.numo_runner import NumoRunner

class CurrencyRunner(NumoRunner):
    def __init__(self):
        self._pattern = r"(\d+(\.\d+)?)\s*([a-zA-Z]+)\s*to\s*([a-zA-Z]+)"
        self._api_url = "https://api.exchangerate-api.com/v4/latest/USD"
        self._exchange_rates: Dict[str, float] = {}
        self._last_update: Optional[datetime] = None
        self._update_interval = timedelta(hours=1)

    async def run(self, source: str) -> Optional[str]:
        """
        Convert between currencies using real-time exchange rates.
        
        Args:
            source: Input string in format "amount currency_from to currency_to"
            
        Returns:
            Converted amount string if successful, None if failed
        """
        match = re.match(self._pattern, source)
        if not match:
            return None

        try:
            await self._update_exchange_rates_if_needed()
            
            amount = float(match.group(1))
            from_currency = match.group(3).upper()
            to_currency = match.group(4).upper()

            converted_amount = self._convert_currency(amount, from_currency, to_currency)
            if converted_amount is not None:
                return f"{converted_amount:.2f} {to_currency}"
                
        except Exception:
            pass

        return None

    async def _update_exchange_rates_if_needed(self) -> None:
        """
        Update exchange rates if they are outdated or not loaded.
        
        Raises:
            Exception: If exchange rates cannot be updated
        """
        now = datetime.now()
        if (not self._exchange_rates or 
            not self._last_update or 
            now - self._last_update > self._update_interval):
            
            await self._fetch_exchange_rates()

    async def _fetch_exchange_rates(self) -> None:
        """
        Fetch current exchange rates from API.
        
        Raises:
            Exception: If API request fails
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(self._api_url) as response:
                if response.status != 200:
                    raise Exception("Failed to update exchange rates")
                    
                data = await response.json()
                self._exchange_rates = data["rates"]
                self._last_update = datetime.now()

    def _convert_currency(self, amount: float, from_currency: str, 
                         to_currency: str) -> Optional[float]:
        """
        Convert amount between currencies using current exchange rates.
        
        Args:
            amount: Amount to convert
            from_currency: Source currency code
            to_currency: Target currency code
            
        Returns:
            Converted amount if conversion is possible, None otherwise
        """
        if (from_currency in self._exchange_rates and 
            to_currency in self._exchange_rates):
            
            from_rate = self._exchange_rates[from_currency]
            to_rate = self._exchange_rates[to_currency]
            
            return amount * (to_rate / from_rate)
            
        return None 