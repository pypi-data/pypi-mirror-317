import logging
import os
import subprocess  # nosec B404 - subprocess used safely with trusted input

from ai_sec.linters.base_linter import BaseLinter
from ai_sec.utils.linter_checker import check_linter_installed

logger = logging.getLogger(__name__)


class TFLintLinter(BaseLinter):

    def __init__(self, framework: str):
        """
        Initialize Tflint with a default framework, which can be overridden via config.
        :param framework: Infrastructure code framework to scan (e.g., 'terraform', 'cloudformation').
        """
        super().__init__(framework)

    def run(self, path):
        """
        Run TFLint with the recursive option and return raw JSON result.

        :param path: Directory path to lint with TFLint.
        :return: Raw JSON string output from TFLint.
        """
        logger.debug(
            f"Received path for TFLint: {path}"
        )  # Add logging to see what is being passed to this method

        if not check_linter_installed("tflint"):
            logger.error(
                "TFLint is not installed. Please install it before running the linter."
            )
            return {"error": "TFLint is not installed"}

        # Ensure the path is absolute
        abs_path = os.path.abspath(path)
        logger.debug(f"Absolute path for TFLint: {abs_path}")  # Log the absolute path

        # Check if the directory exists
        if not os.path.isdir(abs_path):
            logger.error(f"Provided directory does not exist: {abs_path}")
            return {"error": f"Provided directory does not exist: {abs_path}"}

        logger.info(f"Running TFLint recursively on directory: {abs_path}")
        try:
            # Build the command safely
            cmd = ["tflint", "--format", "json", "--recursive"]

            # Using subprocess.run safely with trusted inputs, hence suppressed with nosec
            result = subprocess.run(  # nosec B603
                cmd, capture_output=True, text=True, cwd=abs_path, check=False
            )

            if result.returncode != 0:
                logger.debug(f"TFLint stderr: {result.stderr}")
                if result.stdout:
                    logger.info(
                        "TFLint produced output despite the error. Returning the raw JSON output..."
                    )
                    return result.stdout.strip()
                else:
                    return {
                        "error": f"TFLint failed with return code {result.returncode} and no output."
                    }

            output = result.stdout.strip()
            if not output:
                logger.warning(
                    f"TFLint did not return any output for directory: {abs_path}"
                )
                return {"error": "No output from TFLint"}

            return output  # Return raw JSON string

        # Justify subprocess usage here; suppress Bandit warnings since input is trusted
        except subprocess.CalledProcessError as e:  # nosec
            logger.error(f"Subprocess error occurred while running TFLint: {e}")
            return {"error": f"Unexpected error: {str(e)}"}

        except Exception as e:
            logger.error(f"Unexpected error occurred while running TFLint: {e}")
            return {"error": f"Unexpected error: {str(e)}"}
