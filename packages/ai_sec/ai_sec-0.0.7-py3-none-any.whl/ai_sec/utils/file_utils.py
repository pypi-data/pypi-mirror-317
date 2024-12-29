import logging
import os

logger = logging.getLogger(__name__)


def adjust_paths_generic(result_dict, base_directory):
    """
    Adjust the file paths in the linter results to be relative to the base directory.

    :param result_dict: Parsed result dict of linter issues.
    :param base_directory: Base directory from which paths should be relative.
    :return: Result dict with adjusted paths.
    """
    base_directory = os.path.normpath(base_directory)

    def normalize_path(file_path):
        """
        Helper function to normalize and strip the base directory from the file path.
        """
        full_path = os.path.normpath(file_path)
        relative_path = os.path.relpath(full_path, base_directory)
        logger.debug(f"Normalized {full_path} to {relative_path}")
        return relative_path

    # Adjust paths for TFLint
    for issue in result_dict.get("linters", {}).get("tflint", {}).get("issues", []):
        if "range" in issue and "filename" in issue["range"]:
            issue["range"]["filename"] = normalize_path(issue["range"]["filename"])

    # Adjust paths for TFSec
    for result in result_dict.get("linters", {}).get("tfsec", {}).get("results", []):
        if "location" in result and "filename" in result["location"]:
            result["location"]["filename"] = normalize_path(
                result["location"]["filename"]
            )

    return result_dict


def get_relative_path(full_path, base_directory):
    """
    Get the relative path by stripping the base directory from the full path.

    :param full_path: Full file path.
    :param base_directory: Base directory to be removed.
    :return: Relative file path.
    """
    try:
        logger.info(f"Full path: {full_path}, Base directory: {base_directory}")

        # Normalize both paths (remove any redundant separators)
        full_path = os.path.normpath(full_path)
        base_directory = os.path.normpath(base_directory)

        # Compute the relative path and log it
        relative_path = os.path.relpath(full_path, base_directory)

        # Ensure the path does not go up too far (no '../../../' nonsense)
        if relative_path.startswith(".."):
            # If the relative path goes too far, use the absolute path relative to the base directory
            logger.warning(
                f"Path {relative_path} goes outside the base directory, returning original path."
            )
            return full_path

        logger.info(f"Relative path: {relative_path}")
        return relative_path
    except Exception as e:
        logger.error(
            f"Error getting relative path for '{full_path}' with base directory '{base_directory}': {e}"
        )
        return full_path  # Return full path in case of error
