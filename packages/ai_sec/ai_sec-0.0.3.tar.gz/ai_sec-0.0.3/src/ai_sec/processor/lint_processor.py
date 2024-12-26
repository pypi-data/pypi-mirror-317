from abc import ABC, abstractmethod
from typing import Dict, List


class LinterProcessor(ABC):
    def __init__(self, framework: str):
        """
        Initialize the LinterProcessor with an optional framework.
        :param framework: The infrastructure framework type (e.g., 'terraform', 'cloudformation', 'kubernetes').
        """
        self.framework = framework
        self.linter_data: List[Dict] = []  # Type annotation added here

    @abstractmethod
    def process_data(self, linter_results: Dict) -> List[Dict]:
        """Process linter data and return the formatted result."""
        pass
