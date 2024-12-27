# data_loader.py
import json
import logging
from typing import Dict, List, Optional  # Add Optional for optional parameters

from ai_sec.config import load_config  # Import the config loader

logger = logging.getLogger(__name__)


def load_report(report_path: Optional[str] = None) -> List[Dict]:
    """Load the linting report data from the specified report path or the path in the config."""
    if not report_path:
        config = load_config()
        report_path = config.get("output", {}).get("save_to", "./reports/report.json")

    if not report_path:
        logger.error("Report path is None or empty. Cannot load report.")
        return []  # Return an empty list if the path is invalid

    linter_data = []
    try:
        with open(report_path, "r") as file:
            report = json.load(file)
            for linter_name, linter_results in report.get("linters", {}).items():
                linter_data.extend(linter_results)  # Append all issues directly
        if not linter_data:
            logger.info("No linting issues found in the report.")
        else:
            logger.info(f"Linter data loaded with {len(linter_data)} issues.")
    except FileNotFoundError:
        logger.error(f"Report file not found at: {report_path}")
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from report file: {report_path}")
    return linter_data
