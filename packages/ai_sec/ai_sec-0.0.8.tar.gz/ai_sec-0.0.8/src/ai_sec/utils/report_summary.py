import json
import logging
import os

logger = logging.getLogger(__name__)


def load_report(report_path="./reports/report.json"):
    """
    Load the report data from the specified JSON file.
    
    :param report_path: Path to the main report file.
    :return: A dictionary of report data.
    """
    try:
        with open(report_path, "r") as f:
            report_data = json.load(f)
        # Aggregate all issues across linters into a single list
        all_issues = [
            issue
            for linter_issues in report_data.get("linters", {}).values()
            for issue in linter_issues
        ]
        return all_issues
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        logger.error(f"Failed to load report data from {report_path}: {e}")
        return []


def generate_summary(all_issues):
    """
    Generate a summary of the report data.
    
    :param all_issues: List of all issues from the report.
    :return: A summary dictionary with counts by severity.
    """
    summary = {
        "total_issues": len(all_issues),
        "by_severity": {
            "critical": sum(1 for i in all_issues if i.get("Severity", "").upper() == "CRITICAL"),
            "high": sum(1 for i in all_issues if i.get("Severity", "").upper() == "HIGH"),
            "medium": sum(1 for i in all_issues if i.get("Severity", "").upper() == "MEDIUM"),
            "low": sum(1 for i in all_issues if i.get("Severity", "").upper() == "LOW"),
            "warning": sum(1 for i in all_issues if i.get("Severity", "").upper() == "WARNING"),
        },
    }
    return summary


def save_summary(summary, summary_path="./reports/summary_report.json"):
    """
    Save the summary data to a JSON file.
    
    :param summary: The summary dictionary to save.
    :param summary_path: Path to save the summary file.
    """
    os.makedirs(os.path.dirname(summary_path), exist_ok=True)
    try:
        with open(summary_path, "w") as f:
            json.dump(summary, f, indent=4)
        logger.info(f"Summary report saved to {summary_path}")
    except Exception as e:
        logger.error(f"Failed to save summary report to {summary_path}: {e}")


def generate_and_save_summary(report_path="./reports/report.json", summary_path="./reports/summary_report.json"):
    """
    Load the report, generate a summary, and save it.
    
    :param report_path: Path to the main report file.
    :param summary_path: Path to save the summary file.
    """
    all_issues = load_report(report_path)
    if not all_issues:
        logger.warning("No issues found in the report. Skipping summary generation.")
        return
    
    summary = generate_summary(all_issues)
    save_summary(summary, summary_path)
