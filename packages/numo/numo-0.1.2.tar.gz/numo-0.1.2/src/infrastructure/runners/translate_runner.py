import re
import aiohttp
from typing import Dict, Optional
from src.domain.interfaces.numo_runner import NumoRunner
from src.infrastructure.runners.units import languages

class TranslateRunner(NumoRunner):
    def __init__(self):
        self._pattern = r"(\w+(?:\s+\w+)*)\s+in\s+(\w+)"
        self._base_url = "https://translate.googleapis.com/translate_a/single"
        
    def _get_language_code(self, language: str) -> Optional[str]:
        """
        Get ISO language code from language name.
        
        Args:
            language: Language name (e.g., 'turkish', 'spanish')
            
        Returns:
            Language code (e.g., 'tr', 'es') if found, None otherwise
        """
        language = language.lower()
        
        # If it's a valid language code, return it
        if language in languages:
            return language
            
        # Search for language name in the languages data
        for code, name in languages.items():
            if language in name.lower():
                return code
        return None

    async def run(self, source: str) -> Optional[str]:
        """
        Translate text to specified target language.
        
        Args:
            source: Input string in format "text in language"
            
        Returns:
            Translated text if successful, None otherwise
        """
        match = re.match(self._pattern, source)
        if not match:
            return None

        text = match.group(1)
        target_lang = match.group(2)
        
        lang_code = self._get_language_code(target_lang)
        if not lang_code:
            return None

        try:
            return await self._translate_text(text, lang_code)
        except Exception:
            return None

    async def _translate_text(self, text: str, target_lang: str) -> str:
        """
        Call Google Translate API to translate text.
        
        Args:
            text: Source text to translate
            target_lang: Target language code
            
        Returns:
            Translated text
            
        Raises:
            Exception: If translation fails or response is invalid
        """
        params: Dict[str, str] = {
            "client": "gtx",
            "sl": "auto",  # Source language auto-detection
            "tl": target_lang,
            "dt": "t",  # Return translated text
            "q": text
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(self._base_url, params=params) as response:
                if response.status != 200:
                    raise Exception(f"Translation failed: HTTP {response.status}")
                    
                data = await response.json()
                if not self._is_valid_translation_response(data):
                    raise Exception("Invalid translation response format")
                    
                return data[0][0][0]
    
    def _is_valid_translation_response(self, data: list) -> bool:
        """
        Validate translation API response format.
        
        Args:
            data: Response data from translation API
            
        Returns:
            True if response format is valid, False otherwise
        """
        return (isinstance(data, list) and 
                len(data) > 0 and 
                isinstance(data[0], list) and 
                len(data[0]) > 0 and 
                isinstance(data[0][0], list) and 
                len(data[0][0]) > 0) 