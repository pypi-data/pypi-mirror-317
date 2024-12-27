import os
from typing import Dict, List

from ai_sec.models.checkov_model import CheckovIssue
from ai_sec.processor.ai_processor import AIProcessor  # Import the AIProcessor
from ai_sec.processor.lint_processor import LinterProcessor


class CheckovProcessor(LinterProcessor):

    def __init__(self, framework: str):
        """
        Initialize CheckovProcessor and AIProcessor with the provided framework.
        :param framework: The infrastructure framework being scanned (e.g., 'Terraform', 'CloudFormation').
        """
        super().__init__(framework=framework)
        # Initialize AIProcessor with the provided framework if the OpenAI API key is set
        self.ai_processor = (
            AIProcessor(framework=self.framework)
            if os.getenv("OPENAI_API_KEY")
            else None
        )

        # Variables to store pass/fail summary
        self.total_issues = 0
        self.passed_issues = 0
        self.failed_issues = 0
        self.pass_percentage = 0.0

    def process_data(self, linter_results: Dict) -> List[Dict]:
        """Process Checkov results and append AI-generated severity/context for CRITICAL or HIGH severity."""
        data = []

        # Process failed checks
        for issue in linter_results.get("failed_checks", []):
            self.failed_issues += 1  # Increment failed issues count
            checkov_issue = CheckovIssue(
                check_id=issue.get("check_id"),
                message=issue.get("message"),
                result=issue.get("result", "FAILED"),
                file_path=issue.get("file_path"),
                line_number_start=issue.get("line_number_start"),
                line_number_end=issue.get("line_number_end"),
                severity=issue.get("severity"),
                guideline=issue.get("guideline"),
                resource=issue.get(
                    "resource"
                ),  # Include resource for additional context
            )

            # Collect the initial linter result
            issue_data = {
                "Linter": "Checkov",
                "File": checkov_issue.file_path,
                "Line": checkov_issue.line_range,  # Use line_range property for start - end
                "Description": checkov_issue.message,
                "Severity": (
                    checkov_issue.severity.upper()
                    if checkov_issue.severity
                    else "UNKNOWN"
                ),
                "Context": "",  # Context to be potentially updated by AIProcessor
                "Links": ", ".join(
                    checkov_issue.guideline
                    if isinstance(checkov_issue.guideline, list)
                    else [checkov_issue.guideline] if checkov_issue.guideline else ""
                ),
                "Additional Context": (
                    checkov_issue.resource if checkov_issue.resource else ""
                ),  # Add resource under additional context
            }

            # Use AIProcessor to update severity and context if applicable
            if self.ai_processor:
                issue_data = self.ai_processor.process_linter_issue(issue_data)

            # Append the processed data to the list
            data.append(issue_data)

        # Process passed checks
        for issue in linter_results.get("passed_checks", []):
            self.passed_issues += 1  # Increment passed issues count
            checkov_issue = CheckovIssue(
                check_id=issue.get("check_id"),
                message=issue.get("message"),
                result=issue.get("result", "PASSED"),
                file_path=issue.get("file_path"),
                line_number_start=issue.get("line_number_start"),
                line_number_end=issue.get("line_number_end"),
                severity=issue.get("severity"),
                guideline=issue.get("guideline"),
                resource=issue.get(
                    "resource"
                ),  # Include resource for additional context
            )

            # Collect the initial passed check result
            issue_data = {
                "Linter": "Checkov",
                "File": checkov_issue.file_path,
                "Line": checkov_issue.line_range,  # Use line_range property for start - end
                "Description": checkov_issue.message,
                "Severity": (
                    checkov_issue.severity.upper()
                    if checkov_issue.severity
                    else "UNKNOWN"
                ),
                "Context": "PASSED",
                "Links": ", ".join(
                    checkov_issue.guideline
                    if isinstance(checkov_issue.guideline, list)
                    else [checkov_issue.guideline] if checkov_issue.guideline else ""
                ),
                "Additional Context": (
                    checkov_issue.resource if checkov_issue.resource else ""
                ),  # Add resource under additional context
            }

            # Append the processed data to the list
            data.append(issue_data)

        # Process parsing errors
        for file in linter_results.get("parsing_errors", []):
            parsing_error_data = {
                "Linter": "Checkov",
                "File": file,
                "Line": None,
                "Description": "Parsing error occurred",
                "Severity": "UNKNOWN",
                "Context": "Parsing error",
                "Links": "",
                "Additional Context": "",
            }
            data.append(parsing_error_data)

        # Calculate total issues and pass percentage
        self.total_issues = self.passed_issues + self.failed_issues
        if self.total_issues > 0:
            self.pass_percentage = (self.passed_issues / self.total_issues) * 100

        return data

    def get_summary(self) -> Dict:
        """Get the summary of pass/fail issues and the pass percentage."""
        return {
            "total_issues": self.total_issues,
            "passed_issues": self.passed_issues,
            "failed_issues": self.failed_issues,
            "pass_percentage": self.pass_percentage,
        }
