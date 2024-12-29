import logging
import shutil
from importlib.resources import as_file
from importlib.resources import files as pkg_files
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

from ai_sec import resources  # Assuming `resources` is inside your package

# Set up logging
logger = logging.getLogger(__name__)

# Define the default configuration paths
CONFIG_DIR = Path.home() / ".ai_sec"
CONFIG_FILE = CONFIG_DIR / "config.yaml"
BUNDLED_CONFIG = pkg_files(resources).joinpath("config.yaml")


def ensure_config_exists() -> Path:
    """
    Ensure that the configuration file exists in ~/.ai_sec. If not, copy the bundled resource config.

    Returns:
        Path: The path to the configuration file.
    """
    if not CONFIG_FILE.exists():
        try:
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            # Use `as_file` to get a temporary path for the resource if needed
            with as_file(BUNDLED_CONFIG) as resource_config:
                shutil.copy(str(resource_config), str(CONFIG_FILE))
            logger.info(f"Default configuration copied to {CONFIG_FILE}")
        except Exception as e:
            logger.error(f"Failed to create default config: {e}")
            raise
    else:
        logger.debug(f"Configuration already exists at {CONFIG_FILE}")
    return CONFIG_FILE


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load the configuration from the provided path, the default location (~/.ai_sec/config.yaml),
    or fall back to the bundled resource config in `src/ai_sec/resources/config.yaml`.

    Args:
        config_path (Optional[str]): The path to the configuration file.

    Returns:
        Dict[str, Any]: The loaded configuration data.
    """
    # Determine the configuration file to use
    config_file = Path(config_path) if config_path else CONFIG_FILE

    # If the config file exists, load it
    if config_file.exists():
        try:
            with config_file.open("r") as file:
                primary_config: Dict[str, Any] = yaml.safe_load(file)
                logger.info(f"Loaded configuration from: {config_file}")
                return primary_config
        except Exception as e:
            logger.error(f"Failed to load configuration from {config_file}: {e}")
            raise

    # If no config file exists, fallback to the bundled config
    logger.warning(f"Config file not found at: {config_file}. Falling back to bundled resource.")
    try:
        with as_file(BUNDLED_CONFIG) as resource_config:
            with resource_config.open("r") as file:
                fallback_config: Dict[str, Any] = yaml.safe_load(file)
                logger.info(f"Loaded bundled configuration from: {BUNDLED_CONFIG}")
                return fallback_config
    except Exception as e:
        logger.error(f"Failed to load bundled configuration: {e}")
        raise FileNotFoundError(f"No valid configuration found at {config_file} or in bundled resources.")