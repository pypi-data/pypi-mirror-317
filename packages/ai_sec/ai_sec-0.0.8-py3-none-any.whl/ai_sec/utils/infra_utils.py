import logging
import os
from typing import Optional

# Supported file types for quick detection based on extensions
SUPPORTED_TERRAFORM_FILES = (".tf", ".json")  # Terraform can also be in JSON format
SUPPORTED_CLOUDFORMATION_FILES = (
    ".json",
    ".yaml",
    ".yml",
)  # CloudFormation can be YAML or JSON
SUPPORTED_KUBERNETES_FILES = (
    ".yaml",
    ".yml",
)  # Kubernetes manifests are typically YAML

logger = logging.getLogger(__name__)


def detect_infra_files(directory_path: str) -> Optional[str]:
    """
    Detect the type of infrastructure files present in the directory (Terraform, CloudFormation, or Kubernetes).
    Returns the type of infrastructure detected, or None if none are found.

    :param directory_path: Path to the directory to check.
    :return: 'terraform', 'cloudformation', 'kubernetes', or None
    """
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)

            # Try opening and reading the file
            try:
                with open(file_path, "r") as f:
                    content = f.read()

                # Check for Terraform-specific content
                if file.endswith(SUPPORTED_TERRAFORM_FILES):
                    if any(
                        keyword in content
                        for keyword in ['"terraform"', "resource", "provider"]
                    ):
                        logger.info(f"Terraform files found in {directory_path}")
                        return "terraform"

                # Check for CloudFormation-specific content
                if file.endswith(SUPPORTED_CLOUDFORMATION_FILES):
                    if "AWSTemplateFormatVersion" in content or "Resources" in content:
                        logger.info(f"CloudFormation files found in {directory_path}")
                        return "cloudformation"

                # Check for Kubernetes-specific content
                if file.endswith(SUPPORTED_KUBERNETES_FILES):
                    if "apiVersion" in content and "kind" in content:
                        logger.info(f"Kubernetes files found in {directory_path}")
                        return "kubernetes"

            except (IOError, UnicodeDecodeError) as e:
                logger.error(f"Error reading file {file_path}: {e}")

    logger.error(f"No supported infrastructure files found in {directory_path}.")
    return None
