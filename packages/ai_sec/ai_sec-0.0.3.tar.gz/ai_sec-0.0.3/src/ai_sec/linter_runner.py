import importlib.resources as resources  # Use importlib.resources for resource handling
import json
import logging
import os
import shutil
from typing import Dict

import click

from ai_sec.config import ensure_config_exists, load_config
from ai_sec.lint_factory import LinterFactory  # Import the new LinterFactory
from ai_sec.reporting.dashboard import DashDashboard
from ai_sec.utils.infra_utils import detect_infra_files  # Updated function name
from ai_sec.utils.linter_checker import check_linter_installed
from ai_sec.utils.report_generator import generate_report

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_CONFIG_SOURCE = "src/ai_sec/resources/config.yaml"
DEFAULT_CONFIG_DEST = os.path.expanduser("~/.ai_sec/config.yaml")


@click.group(
    help="""
AI_Sec
Usage:

    ai_sec run <directory> [OPTIONS]
    ai_sec export-config

Commands:
    run            Run the linters on the specified directory and generate a report.
    export-config  Export the default configuration to ~/.ai_sec/config.yaml.

Run 'ai_sec run --help' for more details on the available options.
"""
)
def cli():
    """CLI group for AI_Sec."""
    pass


@cli.command(
    help="""
Run multiple Terraform linters and generate a report. By default, it will
launch the Dash dashboard after the report is generated.

Example:

    ai_sec run ./infra_directory --output json:./reports/report.json

Options:
    directory     The path to the directory containing infrastructure files.
    --config      Path to the configuration file (optional).
    --output      Specify the output format (json or html) and path (optional).
    --no-dash     Do not run the dashboard after linting.
"""
)
@click.argument("directory", type=click.Path(), default=".")
@click.option(
    "--config", type=click.Path(exists=True), help="Path to the configuration file."
)
@click.option(
    "--output", type=str, help="Specify output format (json or html) and path."
)
@click.option("--no-dash", is_flag=True, help="Do not run the dashboard after linting.")
@click.option("--host", default="127.0.0.1", help="Host address for the Dash server.")
@click.option("--port", default=8050, type=int, help="Port number for the Dash server.")
@click.option("--debug", is_flag=True, help="Enable debug mode for the Dash server.")
@click.option(
    "--use-reloader",
    is_flag=True,
    default=True,
    help="Enable or disable the auto-reloader.",
)
def run(directory, config, output, no_dash, host, port, debug, use_reloader):
    """
    Run multiple linters on infrastructure files (Terraform, Kubernetes, CloudFormation) and generate a report.
    By default, it will launch the Dash dashboard after the report is generated.
    """

    # Check if the provided directory exists and is accessible
    if not os.path.isdir(directory):
        logger.error(
            f"Provided directory '{directory}' does not exist or is not accessible."
        )
        click.echo(
            f"Error: Provided directory '{directory}' does not exist or is not accessible."
        )
        return

    # Ensure the config exists
    logger.debug(f"Config file path received: {config}")
    if not config:
        config = ensure_config_exists()
        logger.debug(f"Using default config: {config}")

    # Load the config data
    try:
        config_data = load_config(config)
        logger.debug(f"Config data loaded: {config_data}")
    except FileNotFoundError as e:
        logger.error(f"Configuration file not found: {e}")
        return
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        return

    # Handle output format and path if provided
    if output:
        try:
            output_format, output_path = output.split(":")
            if validate_output_format(output_format):
                config_data["output"]["format"] = output_format
                config_data["output"]["save_to"] = output_path
            else:
                logger.error("Invalid output format specified.")
                return
        except ValueError:
            logger.error(f"Invalid output format argument: {output}")
            return

    # Detect infrastructure type (Terraform, CloudFormation, Kubernetes) and update config
    logger.debug(f"Detecting infrastructure type for directory: {directory}")
    infra_type = detect_infra_files(directory)

    if not infra_type:
        logger.error(
            f"No supported infrastructure files found in directory: {directory}"
        )
        click.echo(
            "Error: No supported infrastructure files found. Please check the directory and try again."
        )
        return

    logger.info(f"Detected {infra_type} files in directory: {directory}")

    # Update the framework in the config for all linters, not just Checkov
    config_data["linters"]["framework"] = infra_type

    # Validate and run linters
    report_path = run_linters_and_generate_report(config_data, directory)
    logger.info(f"Report generated at: {report_path}")

    # Only skip Dash if the user specified `--no-dash`
    if not no_dash:
        base_directory = os.path.abspath(directory)
        logger.info(f"Starting the Dash app with report from: {report_path}")

        # Override host and port with environment variables if running in Docker
        host = os.getenv("HOST", host)
        port = int(os.getenv("PORT", port))

        dashboard = DashDashboard(
            report_path=report_path, base_directory=base_directory
        )
        dashboard.run(
            host=host, port=port, debug=debug, use_reloader=use_reloader
        )  # Pass all parameters


@cli.command(
    help="""
Export the default configuration to ~/.ai_sec/config.yaml.
This command creates the necessary folder and copies the default configuration template.
"""
)
def export_config():
    """Export default config to ~/.ai_sec/config.yaml."""
    config_dir = os.path.dirname(DEFAULT_CONFIG_DEST)

    # Create the directory if it does not exist
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
        logger.info(f"Created directory: {config_dir}")

    # Copy the default config using importlib.resources to access the resource
    if not os.path.exists(DEFAULT_CONFIG_DEST):
        try:
            # Use importlib.resources to get the path to the bundled config.yaml
            with resources.files("ai_sec.resources").joinpath("config.yaml").open(
                "rb"
            ) as fsrc:
                with open(DEFAULT_CONFIG_DEST, "wb") as fdst:
                    shutil.copyfileobj(fsrc, fdst)

            logger.info(f"Config file exported to: {DEFAULT_CONFIG_DEST}")
        except Exception as e:
            logger.error(f"Failed to export config file: {e}")
    else:
        logger.info(f"Config file already exists at: {DEFAULT_CONFIG_DEST}")


def validate_output_format(output_format):
    if output_format not in ["json", "html"]:
        logger.error(
            f"Invalid output format: {output_format}. Supported formats: json, html."
        )
        return False
    return True


def create_processor(ProcessorClass, base_directory, framework):
    """
    Utility function to create a processor instance.
    It checks if 'base_directory' is an argument in the ProcessorClass constructor,
    and initializes it accordingly.

    :param ProcessorClass: The processor class to instantiate.
    :param base_directory: The base directory to be passed if required by the processor.
    :param framework: The framework (e.g., 'terraform', 'cloudformation', 'kubernetes').
    :return: An instance of the processor.
    """
    if "base_directory" in ProcessorClass.__init__.__code__.co_varnames:
        # If the processor accepts base_directory, include it during initialization
        return ProcessorClass(base_directory=base_directory, framework=framework)
    else:
        # If not, just initialize with the framework
        return ProcessorClass(framework=framework)


def run_linter(linter_name, linter_instance, directory: str):
    """
    Runs the specified linter instance and returns raw results or error messages.
    """
    logger.debug(f"Checking if {linter_name} is installed...")
    if check_linter_installed(linter_name):
        logger.info(f"Running {linter_name} on directory: {directory}")
        try:
            return linter_instance.run(directory)  # Pass the correct directory path
        except Exception as e:
            logger.error(f"Failed to run {linter_name}: {e}")
            return {"error": f"Failed to run {linter_name}: {e}"}
    else:
        logger.error(f"{linter_name} is not installed.")
        return {"error": f"{linter_name} is not installed"}


def run_linters_and_generate_report(config: Dict, directory: str) -> str:
    """
    Runs all configured linters, generates, and saves reports.
    :param config: The configuration for the linters and output settings.
    :param directory: The directory to run the linters on.
    :return: The path where the report is saved.
    """
    results = {"summary": {"directory": directory, "linted_files": 0}, "linters": {}}

    # Calculate base directory once
    base_directory = os.path.abspath(directory)

    # Get the enabled linters dynamically from the factory
    linters = LinterFactory.get_enabled_linters(config)

    # Extract the framework from the config, it should be detected before this step
    framework = config["linters"].get("framework")

    if not framework:
        logger.error(f"Framework not detected in the config: {config['linters']}")
        raise ValueError(
            "Framework not detected. Ensure that the infrastructure type is detected and set correctly."
        )

    for linter_name, LinterClass, ResultModel, ProcessorClass in linters:
        logger.debug(f"Running linter {linter_name} for directory {directory}")

        # Properly instantiate the linter with the detected framework
        try:
            linter_instance = LinterClass(framework=framework)
        except TypeError as e:
            logger.error(f"Failed to instantiate {LinterClass.__name__}: {e}")
            continue

        raw_result = run_linter(linter_name, linter_instance, directory)

        # Log the raw result for debugging purposes
        logger.debug(f"Raw result from {linter_name}: {raw_result}")

        # Initialize parsed_json_result to avoid UnboundLocalError
        parsed_json_result = None

        # If raw_result is a string, try to parse it as JSON
        if isinstance(raw_result, str):
            try:
                parsed_json_result = json.loads(raw_result)
                logger.debug(
                    f"Parsed JSON result for {linter_name}: {parsed_json_result}"
                )
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON from {linter_name}: {e}")
                results["linters"][linter_name] = {
                    "error": f"Failed to parse JSON: {e}"
                }
                continue

        # Only proceed if parsing was successful and there is no error in the result
        if parsed_json_result and "error" not in parsed_json_result:
            try:
                # Validate the result model and convert it to a structured format
                parsed_result = ResultModel.from_raw_json(
                    json.dumps(parsed_json_result)
                )
                logger.debug(f"Parsed result for {linter_name}: {parsed_result}")

                # Use the utility function to create the processor
                processor = create_processor(ProcessorClass, base_directory, framework)

                # Process the result
                processed_result = processor.process_data(parsed_result.dict())
                # Save the processed result in the results dictionary
                results["linters"][linter_name] = processed_result
                results["summary"]["linted_files"] += 1  # type: ignore

            except ValueError as e:
                logger.error(f"Failed to process {linter_name} output: {e}")
                results["linters"][linter_name] = {
                    "error": f"Failed to process {linter_name} output: {e}"
                }
        else:
            logger.error(
                f"{linter_name} returned an error: {parsed_json_result.get('error') if parsed_json_result else 'No valid result'}"
            )
            results["linters"][linter_name] = {
                "error": (
                    parsed_json_result.get("error")
                    if parsed_json_result
                    else "No valid result"
                )
            }

    # Check if results contain any linter data before generating the report
    if not results["linters"]:
        logger.warning("No linter results available, skipping report generation.")
        return ""

    # Generate the report
    logger.info("Generating the report based on linter results.")
    generate_report(results, config["output"])
    # Log the final structure of the report for debugging
    logger.debug(f"Final results: {results}")
    return config["output"]["save_to"]  # type: ignore


def main():
    cli()


if __name__ == "__main__":
    main()
