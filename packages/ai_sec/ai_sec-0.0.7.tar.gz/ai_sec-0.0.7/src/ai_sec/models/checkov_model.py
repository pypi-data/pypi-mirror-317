import json
import logging
from typing import List, Optional

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class CheckovIssue(BaseModel):
    check_id: str
    file_path: str
    message: str = "No message available"
    severity: Optional[str] = None
    guideline: Optional[str] = None
    result: str  # PASSED or FAILED
    line_number_start: Optional[int] = None  # Start of the line range
    line_number_end: Optional[int] = None  # End of the line range
    resource: Optional[str] = None  # Resource field for additional context

    @property
    def line_range(self) -> str:
        """Return a formatted line range as 'start - end'."""
        if self.line_number_start is not None and self.line_number_end is not None:
            return f"{self.line_number_start} - {self.line_number_end}"
        return "N/A"

    def __repr__(self):
        """Custom repr method to display issue details."""
        return (
            f"CheckovIssue(\n"
            f"  check_id='{self.check_id}',\n"
            f"  file_path='{self.file_path}',\n"
            f"  message='{self.message}',\n"
            f"  severity='{self.severity or 'None'}',\n"
            f"  guideline='{self.guideline or 'None'}',\n"
            f"  result='{self.result}',\n"
            f"  line_number_start={self.line_number_start},\n"
            f"  line_number_end={self.line_number_end},\n"
            f"  line_range='{self.line_range}',\n"
            f"  resource='{self.resource}'\n"
            f")"
        )


class CheckovSummary(BaseModel):
    passed: int
    failed: int
    skipped: int
    parsing_errors: int
    resource_count: int
    checkov_version: str


class CheckovResult(BaseModel):
    summary: Optional[CheckovSummary]
    failed_checks: List[CheckovIssue] = []
    passed_checks: List[CheckovIssue] = []
    parsing_errors: List[str] = []  # List of files that had parsing errors

    @classmethod
    def from_raw_json(cls, raw_json: str) -> "CheckovResult":
        """
        Factory method to parse the relevant fields from the Checkov JSON.
        :param raw_json: Raw JSON output from Checkov.
        :return: CheckovResult object containing parsed checks and summary.
        """
        try:
            parsed_json = json.loads(raw_json)

            # Parse the failed, passed checks, and parsing errors
            failed_checks = cls._parse_checks(
                parsed_json.get("results", {}).get("failed_checks", []), "FAILED"
            )
            passed_checks = cls._parse_checks(
                parsed_json.get("results", {}).get("passed_checks", []), "PASSED"
            )
            parsing_errors = parsed_json.get("results", {}).get("parsing_errors", [])

            # Parse summary details if available
            summary_data = parsed_json.get("summary", None)
            summary = CheckovSummary(**summary_data) if summary_data else None

            return cls(
                failed_checks=failed_checks,
                passed_checks=passed_checks,
                parsing_errors=parsing_errors,
                summary=summary,
            )

        except Exception as e:
            logger.error(f"Error parsing Checkov JSON: {e}")
            raise ValueError(f"Invalid Checkov result format: {e}")

    @staticmethod
    def _parse_checks(checks: List[dict], result_type: str) -> List[CheckovIssue]:
        """
        Helper method to parse passed or failed checks.
        :param checks: List of check dictionaries from Checkov output.
        :param result_type: Result type ('PASSED' or 'FAILED').
        :return: List of CheckovIssue objects.
        """
        parsed_checks = []
        for check in checks:
            file_line_range = check.get("file_line_range", [None, None])
            line_number_start, line_number_end = (
                file_line_range if len(file_line_range) == 2 else (None, None)
            )

            parsed_checks.append(
                CheckovIssue(
                    check_id=check.get(
                        "check_id", ""
                    ),  # Default to empty string if None
                    file_path=check.get(
                        "file_path", ""
                    ),  # Default to empty string if None
                    message=check.get("check_name", "No message available"),
                    severity=check.get("severity"),
                    guideline=check.get("guideline"),
                    result=result_type,
                    line_number_start=line_number_start,
                    line_number_end=line_number_end,
                    resource=check.get("resource"),  # Include the resource field
                )
            )
        return parsed_checks

    def __repr__(self):
        """Custom repr method to display CheckovResult summary."""
        return (
            f"CheckovResult(\n"
            f"  Summary: {self.summary},\n"
            f"  Passed Checks: {len(self.passed_checks)},\n"
            f"  Failed Checks: {len(self.failed_checks)},\n"
            f"  Parsing Errors: {len(self.parsing_errors)} files\n"
            f")"
        )
