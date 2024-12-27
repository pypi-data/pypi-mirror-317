import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class BaseDashboard(ABC):
    """
    Abstract class for dashboard implementations.
    This allows for flexibility in choosing a specific dashboard solution.
    """

    def __init__(self, report_path):
        self.report_path = report_path

    @abstractmethod
    def load_report(self):
        """
        Load the report from the file system.
        This should be implemented by the subclass.
        """
        pass

    @abstractmethod
    def preprocess_data(self):
        """
        Preprocess the report data for visualization.
        This should be implemented by the subclass.
        """
        pass

    @abstractmethod
    def run(self):
        """
        Run the dashboard application.
        This should be implemented by the subclass.
        """
        pass
