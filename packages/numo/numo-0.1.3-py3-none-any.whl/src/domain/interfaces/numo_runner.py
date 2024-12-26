from abc import ABC, abstractmethod
from typing import Optional

class NumoRunner(ABC):
    @abstractmethod
    async def run(self, source: str) -> Optional[str]:
        """Run the processor on the source string."""
        pass 