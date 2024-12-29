import logging
import shutil
import subprocess  # nosec B404 - subprocess used safely with trusted input

logger = logging.getLogger(__name__)


def check_linter_installed(linter_name, version_command=["--version"]):
    """
    Check if a linter is installed by running its version command.

    :param linter_name: Name of the linter to check.
    :param version_command: Command to check the version of the linter.
    :return: True if installed, False if not.
    """
    linter_path = shutil.which(linter_name)
    if linter_path is None:
        logger.error(
            f"{linter_name} is not installed. Please install it to use this tool."
        )
        return False

    try:
        # Run the version command safely without shell=True
        subprocess.run(
            [linter_name] + version_command, capture_output=True, check=True
        )  # nosec B603
        logger.info(f"{linter_name} is installed and available at {linter_path}.")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error checking {linter_name}: {e}. Return code: {e.returncode}")
        return False
    except FileNotFoundError:
        logger.error(
            f"{linter_name} not found. Please ensure it is properly installed."
        )
        return False
    except Exception as e:
        logger.error(f"Unexpected error while checking {linter_name}: {e}")
        return False
