import os
from typing import Dict, List

from ai_sec.models.tflint_model import TFLintIssue
from ai_sec.processor.ai_processor import AIProcessor
from ai_sec.processor.lint_processor import LinterProcessor


class TFLintProcessor(LinterProcessor):

    def __init__(self, framework: str):
        super().__init__(framework=framework)
        # Initialize AIProcessor if OpenAI API key is set
        self.ai_processor = (
            AIProcessor(framework=self.framework)
            if os.getenv("OPENAI_API_KEY")
            else None
        )

    def process_data(self, linter_results: Dict) -> List[Dict]:
        """Process TFLint results and append AI-generated context if applicable."""
        data = []
        for issue in linter_results.get("issues", []):
            tflint_issue = TFLintIssue.parse_obj(issue)

            # Initial issue data
            issue_data = {
                "Linter": "TFLint",
                "File": tflint_issue.get_file_path(),
                "Line": tflint_issue.range.start["line"],
                "Description": tflint_issue.message,
                "Severity": tflint_issue.rule.severity.upper(),
                "Context": "",  # AI-generated context placeholder
                "Links": [tflint_issue.rule.link] if tflint_issue.rule.link else [],
            }

            # Use AIProcessor for critical or high-severity issues
            if self.ai_processor and tflint_issue.rule.severity.upper() in {
                "CRITICAL",
                "HIGH",
            }:
                issue_data = self.ai_processor.process_linter_issue(issue_data)

            data.append(issue_data)
        return data
