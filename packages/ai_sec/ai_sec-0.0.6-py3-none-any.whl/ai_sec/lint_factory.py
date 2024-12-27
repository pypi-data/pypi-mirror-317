import logging
from typing import Dict, List, Tuple, Type

from ai_sec.linters.checkov import CheckovLinter
from ai_sec.linters.tflint import TFLintLinter
from ai_sec.linters.tfsec import TFSecLinter
from ai_sec.models.checkov_model import CheckovResult
from ai_sec.models.tflint_model import TFLintResult
from ai_sec.models.tfsec_model import TFSecReport
from ai_sec.processor.checkov_processor import CheckovProcessor
from ai_sec.processor.tflint_processor import TFLintProcessor
from ai_sec.processor.tfsec_processor import TFSecProcessor

logger = logging.getLogger(__name__)


class LinterFactory:
    """
    Factory class to dynamically return the appropriate Linter, Model, and Processor
    based on configuration, including the correct framework for each linter.
    """

    # Define a mapping between linter names and their classes
    LINTER_MAP: Dict[str, Tuple[Type, Type, Type]] = {
        "tflint": (TFLintLinter, TFLintResult, TFLintProcessor),
        "tfsec": (TFSecLinter, TFSecReport, TFSecProcessor),
        "checkov": (CheckovLinter, CheckovResult, CheckovProcessor),
    }

    # Define a mapping of supported frameworks per linter
    SUPPORTED_FRAMEWORKS = {
        "tflint": ["terraform"],  # TFLint only supports Terraform
        "tfsec": [
            "terraform",
            "cloudformation",
        ],  # TFSec supports Terraform and CloudFormation
        "checkov": [
            "terraform",
            "cloudformation",
            "kubernetes",
        ],  # Checkov supports all three
    }

    @staticmethod
    def get_enabled_linters(config: Dict) -> list:
        """
        Dynamically get the list of enabled linters based on the config and the detected infra framework.
        :param config: The configuration dictionary.
        :return: A list of tuples containing the linter name, LinterClass, ResultModel, and ProcessorClass.
        """
        enabled_linters: List[Tuple[str, Type, Type, Type]] = []

        # Get the infra type (framework) from the higher level in the config
        infra_type = config["linters"].get("framework")
        if not infra_type:
            logger.error("Framework not set in config; cannot detect infra type.")
            return enabled_linters

        # Loop through the linter map and check if the linter supports the detected framework
        for linter_name, (
            LinterClass,
            ResultModel,
            ProcessorClass,
        ) in LinterFactory.LINTER_MAP.items():
            # Check if the linter is enabled in the config and if it supports the detected infra type
            if config["linters"].get(linter_name, {}).get("enabled", False):
                if infra_type in LinterFactory.SUPPORTED_FRAMEWORKS.get(
                    linter_name, []
                ):
                    enabled_linters.append(
                        (linter_name, LinterClass, ResultModel, ProcessorClass)
                    )
                else:
                    logger.debug(
                        f"Linter {linter_name} does not support framework {infra_type}. Skipping..."
                    )

        return enabled_linters
