import logging
from abc import ABC, abstractmethod

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class BaseLinter(ABC):
    def __init__(self, framework: str):
        """
        Initialize the base linter with the specified framework.
        :param framework: Infrastructure code framework (e.g., 'terraform', 'cloudformation').
        """
        self.framework = framework

    @abstractmethod
    def run(self, directory):
        """
        Abstract method that must be implemented by subclasses.
        This method will be responsible for running the linter
        with the given directory and returning the results.
        :param directory: The root directory containing the infrastructure files.
        :return: A dictionary representing the linter results (e.g., errors, warnings).
        """
        pass

    def parse_output(self, output):
        """
        Optional method to parse the raw output of the linter.
        By default, this just returns the raw output, but subclasses
        can override this method to perform custom parsing.

        :param output: The raw output from the linter (as a string).
        :return: Parsed output (e.g., JSON, dictionary).
        """
        logger.info("Parsing output")
        return output
