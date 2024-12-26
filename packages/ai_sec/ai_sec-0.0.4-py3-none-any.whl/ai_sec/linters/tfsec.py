import json
import logging
import os
import subprocess  # nosec B404 - subprocess used safely with trusted input

from ai_sec.linters.base_linter import BaseLinter
from ai_sec.utils.linter_checker import check_linter_installed

logger = logging.getLogger(__name__)


class TFSecLinter(BaseLinter):

    def __init__(self, framework: str):
        """
        Initialize CheckovLinter with a default framework, which can be overridden via config.
        :param framework: Infrastructure code framework to scan (e.g., 'terraform', 'cloudformation').
        """
        super().__init__(framework)

    def run(self, path):
        """
        Run TFSec on the provided directory path and return raw JSON result.

        :param path: Directory path to lint with TFSec.
        :return: Raw JSON string output from TFSec.
        """
        if not check_linter_installed("tfsec"):
            logger.error(
                "TFSec is not installed. Please install it before running the linter."
            )
            return {"error": "TFSec is not installed"}

        # Ensure the path is absolute
        abs_path = os.path.abspath(path)

        # Check if the directory exists
        if not os.path.isdir(abs_path):
            logger.error(f"Provided directory does not exist: {abs_path}")
            return {"error": f"Provided directory does not exist: {abs_path}"}

        logger.info(f"Running TFSec on directory: {abs_path}")

        try:
            # Command to run TFSec with the required options
            cmd = ["tfsec", "--format", "json"]  # Safely built as a list

            # Run the tfsec command safely using subprocess with no shell=True
            result = subprocess.run(  # nosec B603 - trusted input, no shell execution
                cmd, capture_output=True, text=True, cwd=abs_path, check=False
            )

            logger.info(f"TFSec completed with return code {result.returncode}")

            if result.returncode != 0:
                logger.error(f"TFSec failed with return code {result.returncode}")
                logger.debug(f"TFSec stderr: {result.stderr}")
                # Log stdout if any output is produced
                if result.stdout:
                    logger.warning(
                        "TFSec produced output despite the error. Returning the partial JSON output..."
                    )
                    return self.adjust_paths_in_result(
                        result.stdout.strip(), abs_path
                    )  # Adjust paths here

                return {
                    "error": f"TFSec failed with return code {result.returncode} and no valid output."
                }

            output = result.stdout.strip()
            if not output:
                logger.warning(
                    f"TFSec did not return any output for directory: {abs_path}"
                )
                return {"error": "No output from TFSec"}

            # Adjust file paths to be relative before returning
            return self.adjust_paths_in_result(output, abs_path)

        except FileNotFoundError as fnf_error:
            logger.error(f"File not found during TFSec execution: {fnf_error}")
            return {"error": f"File not found: {fnf_error}"}

        except subprocess.CalledProcessError as cpe:  # nosec
            logger.error(f"Subprocess error occurred while running TFSec: {cpe}")
            return {"error": f"Subprocess error: {str(cpe)}"}

        except Exception as e:
            logger.error(f"Unexpected error occurred while running TFSec: {e}")
            return {"error": f"Unexpected error: {str(e)}"}

    def adjust_paths_in_result(self, raw_output, base_path):
        """
        Adjust the file paths in the TFSec result to be relative to the base directory.

        :param raw_output: The raw JSON output from TFSec.
        :param base_path: The base directory path from which paths should be relative.
        :return: The modified JSON result with relative paths.
        """
        try:
            result = json.loads(raw_output)
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing TFSec output JSON: {e}")
            return {"error": f"Error parsing TFSec output JSON: {e}"}

        for issue in result.get("results", []):
            # Adjust the filename path to be relative
            try:
                if "location" in issue and "filename" in issue["location"]:
                    abs_filename = issue["location"]["filename"]
                    relative_path = os.path.relpath(abs_filename, base_path)

                    if not os.path.exists(abs_filename):
                        logger.warning(
                            f"File {abs_filename} does not exist. Leaving the path unchanged."
                        )
                    else:
                        issue["location"]["filename"] = relative_path
                        logger.info(f"Adjusted file path to relative: {relative_path}")
            except KeyError as ke:
                logger.error(f"Key error in TFSec result structure: {ke}")
                continue
            except Exception as e:
                logger.error(f"Error adjusting paths in TFSec result: {e}")

        return json.dumps(result, indent=4)
