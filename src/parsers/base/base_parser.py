from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseParser(ABC):

    @abstractmethod
    def url(self, criteria: Dict[str, str]) -> str:
        pass

    @abstractmethod
    def parse_resume(self) -> List[Dict[str, Any]]:
        pass