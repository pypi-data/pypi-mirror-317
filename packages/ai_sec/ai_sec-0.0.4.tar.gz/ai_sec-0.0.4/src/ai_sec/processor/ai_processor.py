import os
from typing import Dict

from ai_sec.ai_assist.issue_handler import IssueHandler


class AIProcessor:
    def __init__(self, framework: str):
        self.framework = framework
        self.ai_handler = None
        if os.getenv("OPENAI_API_KEY"):
            self.ai_handler = IssueHandler()

    def process_linter_issue(self, issue_data: Dict) -> Dict:
        """
        Processes a linter result by checking and updating severity/context using AI.
        :param issue_data: Dictionary containing linter issue details.
        :return: Updated issue data with inferred severity or context (if applicable).
        """
        # Infer severity if it's UNKNOWN
        severity = issue_data.get("Severity", "UNKNOWN").upper()
        if severity == "UNKNOWN" and self.ai_handler:
            inferred_severity = self.ai_handler.infer_severity(
                issue_data["Description"], self.framework
            )
            issue_data["Severity"] = inferred_severity or severity

        # Add context for CRITICAL or HIGH severity issues
        if issue_data["Severity"] in ["CRITICAL", "HIGH", "MEDIUM"] and self.ai_handler:
            issue_data["Context"] = self.ai_handler.generate_resolution_context(
                issue_data["Description"], self.framework
            )

        return issue_data
