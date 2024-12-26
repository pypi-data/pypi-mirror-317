import json
import logging
import os
import shutil
import subprocess  # nosec B404 - subprocess used safely with trusted input
from typing import Dict, List, Union

from ai_sec.linters.base_linter import BaseLinter
from ai_sec.models.checkov_model import (  # Import CheckovResult
    CheckovIssue,
    CheckovResult,
)
from ai_sec.utils.linter_checker import check_linter_installed

logger = logging.getLogger(__name__)


class CheckovLinter(BaseLinter):
    def __init__(self, framework: str):
        """
        Initialize CheckovLinter with a default framework, which can be overridden via config.
        :param framework: Infrastructure code framework to scan (e.g., 'terraform', 'cloudformation').
        """
        super().__init__(framework)

    def run(self, path):
        """
        Run Checkov on the provided directory path and return raw JSON result.

        :param path: Directory path to lint with Checkov.
        :return: Raw JSON string output from Checkov.
        """
        logger.debug(f"Received path for Checkov: {path}")

        # Ensure Checkov is installed
        if not check_linter_installed("checkov"):
            logger.error(
                "Checkov is not installed. Please install it before running the linter."
            )
            return {"error": "Checkov is not installed"}

        # Resolve the full path of the checkov executable
        checkov_path = shutil.which("checkov")
        if checkov_path is None:
            logger.error("Could not find Checkov executable in PATH.")
            return {"error": "Checkov is not installed or not found in PATH"}

        # Ensure the path is absolute
        abs_path = os.path.abspath(path)
        logger.debug(f"Absolute path for Checkov: {abs_path}")

        # Check if the directory exists
        if not os.path.isdir(abs_path):
            logger.error(f"Provided directory does not exist: {abs_path}")
            return {"error": f"Provided directory does not exist: {abs_path}"}

        logger.info(
            f"Running Checkov on directory: {abs_path} with framework: {self.framework}"
        )

        try:
            # Build the command using a list
            cmd = [
                checkov_path,
                "-d",
                abs_path,
                "--output",
                "json",
                "--framework",
                self.framework,
                "--compact",
            ]

            # Using subprocess.run safely with trusted inputs, hence suppressed with nosec
            result = subprocess.run(  # nosec B603
                cmd, capture_output=True, text=True, cwd=abs_path, check=False
            )

            # Handle cases where Checkov fails or returns errors
            if result.returncode != 0:
                logger.debug(f"Checkov stderr: {result.stderr}")
                if result.stdout:
                    logger.info(
                        "Checkov produced output despite the error. Returning the raw JSON output..."
                    )
                    logger.info(f"Checkov stdout: {result.stdout}")
                    return result.stdout.strip()
                else:
                    return {
                        "error": f"Checkov failed with return code {result.returncode} and no output."
                    }

            output = result.stdout.strip()
            if not output:
                logger.warning(
                    f"Checkov did not return any output for directory: {abs_path}"
                )
                return {"error": "No output from Checkov"}

            return output  # Return raw JSON string

        except subprocess.CalledProcessError as e:  # nosec
            logger.error(f"Subprocess error occurred while running Checkov: {e}")
            return {"error": f"Unexpected error: {str(e)}"}

        except Exception as e:
            logger.error(f"Unexpected error occurred while running Checkov: {e}")
            return {"error": f"Unexpected error: {str(e)}"}


def _parse_checkov_result(
    self, raw_output: str
) -> Dict[str, Union[List[CheckovIssue], Dict[str, object]]]:
    """
    Parse the Checkov output and convert it into a structured format using CheckovResult.
    :param raw_output: Raw JSON string output from Checkov.
    :return: Parsed result containing failed and passed checks, with the summary as a dictionary.
    """
    try:
        checkov_result = CheckovResult.from_raw_json(raw_output)

        failed_checks: List[CheckovIssue] = (
            checkov_result.failed_checks if checkov_result.failed_checks else []
        )
        passed_checks: List[CheckovIssue] = (
            checkov_result.passed_checks if checkov_result.passed_checks else []
        )

        summary = (
            checkov_result.summary.dict()
            if checkov_result.summary
            else {
                "passed": 0,
                "failed": 0,
                "skipped": 0,
                "parsing_errors": 0,
                "resource_count": 0,
                "checkov_version": "unknown",
            }
        )

        parsed_result: Dict[str, Union[List[CheckovIssue], Dict[str, object]]] = {
            "failed_checks": failed_checks,
            "passed_checks": passed_checks,
            "summary": summary,
        }

        return parsed_result

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Checkov output: {e}")
        return {
            "failed_checks": [],
            "passed_checks": [],
            "summary": {
                "passed": 0,
                "failed": 0,
                "skipped": 0,
                "parsing_errors": 0,
                "resource_count": 0,
                "checkov_version": "unknown",
            },
        }
