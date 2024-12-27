import json
import logging
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape

logger = logging.getLogger(__name__)


def generate_report(results, output_config):
    """
    Generate the final report based on the results and the configuration.

    :param results: Results from all linters.
    :param output_config: Output format and file location (JSON or HTML).
    """
    # Ensure the directory exists
    output_dir = os.path.dirname(output_config["save_to"])
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logger.info(f"Created output directory: {output_dir}")

    if output_config["format"] == "json":
        try:
            with open(output_config["save_to"], "w") as file:
                json.dump(results, file, indent=4)
            logger.info(f"JSON report saved to {output_config['save_to']}")
        except Exception as e:
            logger.error(f"Failed to save JSON report: {e}")

    elif output_config["format"] == "html":
        try:
            # Enable autoescape for HTML and XML files to prevent XSS attacks
            env = Environment(
                loader=FileSystemLoader(output_config.get("template_dir", "templates")),
                autoescape=select_autoescape(["html", "xml"]),  # Autoescape enabled
            )
            template = env.get_template("report_template.html")
            output = template.render(results=results)
            with open(output_config["save_to"], "w") as file:
                file.write(output)
            logger.info(f"HTML report saved to {output_config['save_to']}")
        except Exception as e:
            logger.error(f"Failed to generate or save HTML report: {e}")
    else:
        logger.error(f"Unsupported report format: {output_config['format']}")
