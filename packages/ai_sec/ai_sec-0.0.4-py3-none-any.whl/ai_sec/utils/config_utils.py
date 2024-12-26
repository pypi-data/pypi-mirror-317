import logging
import os

import yaml

logger = logging.getLogger(__name__)


def load_config(config_file):
    """
    Load configuration from the specified YAML file.

    :param config_file: Path to the YAML configuration file.
    :return: Parsed configuration as a dictionary.
    """
    if not os.path.exists(config_file):
        logger.error(f"Configuration file {config_file} does not exist.")
        raise FileNotFoundError(f"Configuration file {config_file} not found.")
    with open(config_file, "r") as file:
        try:
            logger.info("Configuration found at {}", config_file)
            return yaml.safe_load(file)
        except yaml.YAMLError as e:
            logger.error(f"Error loading configuration: {e}")
            raise
