from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseAnalyzer(ABC):
    @abstractmethod
    async def analyze(self, code: str, filename: str) -> List[Dict[str, Any]]:
        """Analyze code and return list of issues"""
        pass
    
    @abstractmethod
    def get_metrics(self, code: str) -> Dict[str, Any]:
        """Get code metrics like complexity, lines of code, etc."""
        pass