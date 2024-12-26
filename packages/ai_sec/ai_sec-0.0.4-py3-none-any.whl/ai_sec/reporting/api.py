# src/ai_sec/reporting/api.py
import json
import logging

from flask import Blueprint, jsonify, request

from ai_sec.config import load_config

logger = logging.getLogger(__name__)
api_bp = Blueprint("api", __name__)

# Load the report data at the start of the application
config = load_config()
report_path = config.get("output", {}).get("save_to", "./reports/report.json")

try:
    with open(report_path, "r") as f:
        report_data = json.load(f)
    # Aggregate all issues across linters into a single list
    all_issues = [
        issue
        for linter_issues in report_data.get("linters", {}).values()
        for issue in linter_issues
    ]
except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
    logger.error(f"Failed to load report data: {e}")
    all_issues = []  # Fallback to an empty list if loading fails


@api_bp.route("/api/report", methods=["GET"])
def get_full_report():
    """Endpoint to retrieve the full report."""
    return jsonify({"issues": all_issues})


@api_bp.route("/api/report/summary", methods=["GET"])
def get_report_summary():
    """Endpoint to retrieve a summary of the report."""
    summary = {
        "total_issues": len(all_issues),
        "by_severity": {
            "critical": sum(
                1 for i in all_issues if i["Severity"].upper() == "CRITICAL"
            ),
            "high": sum(1 for i in all_issues if i["Severity"].upper() == "HIGH"),
            "medium": sum(1 for i in all_issues if i["Severity"].upper() == "MEDIUM"),
            "low": sum(1 for i in all_issues if i["Severity"].upper() == "LOW"),
            "warning": sum(1 for i in all_issues if i["Severity"].upper() == "WARNING"),
        },
    }
    return jsonify(summary)


@api_bp.route("/api/report/issues", methods=["GET"])
def get_filtered_issues():
    """Endpoint to retrieve filtered issues by severity."""
    severity = request.args.get("severity")
    filtered_issues = (
        [i for i in all_issues if i["Severity"].upper() == severity.upper()]
        if severity
        else all_issues
    )
    return jsonify(filtered_issues)
