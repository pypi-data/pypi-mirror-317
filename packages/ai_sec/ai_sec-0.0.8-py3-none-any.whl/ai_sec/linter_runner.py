import importlib.resources as resources  # Use importlib.resources for resource handling
import json
import logging
import os
import shutil

import click

from ai_sec.config import ensure_config_exists, load_config
from ai_sec.lint_factory import LinterFactory
from ai_sec.reporting.dashboard import DashDashboard
from ai_sec.utils.infra_utils import detect_infra_files
from ai_sec.utils.linter_checker import check_linter_installed
from ai_sec.utils.report_generator import generate_report
from ai_sec.utils.report_summary import generate_and_save_summary
from ai_sec.utils.report_to_html import generate_html_report

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
    --output      Specify output format (json or html) and path (optional).
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
    Run multiple linters on infrastructure files and generate a report.
    """
    if not os.path.isdir(directory):
        logger.error(f"Provided directory '{directory}' does not exist or is not accessible.")
        click.echo(f"Error: Provided directory '{directory}' does not exist or is not accessible.")
        return

    config_data = initialize_config(config, output)
    if not config_data:
        return

    infra_type = detect_infra_files(directory)
    if not infra_type:
        logger.error(f"No supported infrastructure files found in directory: {directory}")
        click.echo("Error: No supported infrastructure files found. Please check the directory and try again.")
        return

    logger.info(f"Detected {infra_type} files in directory: {directory}")
    config_data["linters"]["framework"] = infra_type

    report_path = run_linters_and_generate_report(config_data, directory)
    logger.info(f"Report generated at: {report_path}")

    if not no_dash:
        launch_dashboard(report_path, directory, host, port, debug, use_reloader)


@cli.command(
    help="""
Export the default configuration to ~/.ai_sec/config.yaml.
This command creates the necessary folder and copies the default configuration template.
"""
)
def export_config():
    """Export default config to ~/.ai_sec/config.yaml."""
    config_dir = os.path.dirname(DEFAULT_CONFIG_DEST)

    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
        logger.info(f"Created directory: {config_dir}")

    if not os.path.exists(DEFAULT_CONFIG_DEST):
        try:
            with resources.files("ai_sec.resources").joinpath("config.yaml").open("rb") as fsrc:
                with open(DEFAULT_CONFIG_DEST, "wb") as fdst:
                    shutil.copyfileobj(fsrc, fdst)
            logger.info(f"Config file exported to: {DEFAULT_CONFIG_DEST}")
        except Exception as e:
            logger.error(f"Failed to export config file: {e}")
    else:
        logger.info(f"Config file already exists at: {DEFAULT_CONFIG_DEST}")


def initialize_config(config, output):
    """Initialize configuration data."""
    if not config:
        config = ensure_config_exists()
    try:
        config_data = load_config(config)
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        return None

    if output:
        try:
            output_format, output_path = output.split(":")
            if validate_output_format(output_format):
                config_data["output"]["format"] = output_format
                config_data["output"]["save_to"] = output_path
            else:
                return None
        except ValueError:
            logger.error(f"Invalid output format argument: {output}")
            return None
    return config_data


def validate_output_format(output_format):
    if output_format not in ["json", "html"]:
        logger.error(f"Invalid output format: {output_format}. Supported formats: json, html.")
        return False
    return True


def create_processor(ProcessorClass, base_directory, framework):
    """Create a processor instance."""
    if "base_directory" in ProcessorClass.__init__.__code__.co_varnames:
        return ProcessorClass(base_directory=base_directory, framework=framework)
    return ProcessorClass(framework=framework)


def run_linter(linter_name, linter_instance, directory):
    """Run a linter and return results."""
    logger.debug(f"Checking if {linter_name} is installed...")
    if check_linter_installed(linter_name):
        try:
            return linter_instance.run(directory)
        except Exception as e:
            logger.error(f"Failed to run {linter_name}: {e}")
            return {"error": f"Failed to run {linter_name}: {e}"}
    logger.error(f"{linter_name} is not installed.")
    return {"error": f"{linter_name} is not installed"}


def run_linters_and_generate_report(config, directory):
    """Run all linters, process results, and generate reports."""
    results = {"summary": {"directory": directory, "linted_files": 0}, "linters": {}}
    base_directory = os.path.abspath(directory)
    linters = LinterFactory.get_enabled_linters(config)
    framework = config["linters"].get("framework")

    if not framework:
        raise ValueError("Framework not detected. Ensure the infrastructure type is set.")

    for linter_name, LinterClass, ResultModel, ProcessorClass in linters:
        try:
            linter_instance = LinterClass(framework=framework)
            raw_result = run_linter(linter_name, linter_instance, directory)

            if isinstance(raw_result, str):
                parsed_json = json.loads(raw_result)
                if "error" not in parsed_json:
                    parsed_result = ResultModel.from_raw_json(json.dumps(parsed_json))
                    processor = create_processor(ProcessorClass, base_directory, framework)
                    processed_result = processor.process_data(parsed_result.dict())
                    results["linters"][linter_name] = processed_result
                    results["summary"]["linted_files"] += 1
        except Exception as e:
            logger.error(f"Exception occurred while running {linter_name}: {e}")
            results["linters"][linter_name] = {"error": f"Exception: {e}"}

    if results["linters"]:
        generate_reports(results, config)
    else:
        logger.warning("No linter results available, skipping report generation.")
    return config["output"]["save_to"]


def generate_reports(results, config):
    """Generate JSON, summary, and HTML reports."""
    # Determine the reports directory
    report_path = config["output"]["save_to"]
    reports_dir = os.path.dirname(report_path)
    summary_path = os.path.join(reports_dir, "summary_report.json")
    html_report_path = os.path.join(reports_dir, "report.html")

    # Ensure the reports directory exists
    os.makedirs(reports_dir, exist_ok=True)

    # Generate JSON report
    generate_report(results, config["output"])

    # Generate summary report
    generate_and_save_summary(report_path, summary_path)
    logger.info(f"Summary report saved to: {summary_path}")

    # Generate HTML report
    try:
        css_path = resources.files("ai_sec.resources").joinpath("custom_styles.css")
        generate_html_report(
            input_file=report_path,
            summary_file=summary_path,
            output_file=html_report_path,
            css_file=str(css_path),
        )
        logger.info(f"HTML report saved to: {html_report_path}")
    except Exception as e:
        logger.error(f"Failed to generate HTML report: {e}")


def launch_dashboard(report_path, directory, host, port, debug, use_reloader):
    """Launch the Dash dashboard."""
    base_directory = os.path.abspath(directory)
    dashboard = DashDashboard(report_path=report_path, base_directory=base_directory)
    dashboard.run(host=host, port=port, debug=debug, use_reloader=use_reloader)


def main():
    cli()


if __name__ == "__main__":
    main()