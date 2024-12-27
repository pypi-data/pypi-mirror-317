import os
from typing import Dict, List

from ai_sec.models.tfsec_model import TFSecResult
from ai_sec.processor.ai_processor import AIProcessor
from ai_sec.processor.lint_processor import LinterProcessor


class TFSecProcessor(LinterProcessor):

    def __init__(self, framework: str, base_directory=None):
        super().__init__(framework=framework)
        self.base_directory = base_directory
        # Initialize AIProcessor if OpenAI API key is set
        self.ai_processor = (
            AIProcessor(framework=self.framework)
            if os.getenv("OPENAI_API_KEY")
            else None
        )

    def process_data(self, linter_results: Dict) -> List[Dict]:
        """Process TFSec results and append AI-generated context if applicable."""
        data = []
        for result in linter_results.get("results", []):
            tfsec_result = TFSecResult.parse_obj(result)

            # Initial issue data
            issue_data = {
                "Linter": "TFSec",
                "File": tfsec_result.get_file_path(self.base_directory),
                "Line": tfsec_result.location.start_line,
                "Description": tfsec_result.rule_description,
                "Severity": tfsec_result.severity.upper(),
                "Context": "",  # AI-generated context placeholder
                "Links": tfsec_result.links,
            }

            # Use AIProcessor for critical or high-severity issues
            if self.ai_processor and tfsec_result.severity.upper() in {
                "CRITICAL",
                "HIGH",
            }:
                issue_data = self.ai_processor.process_linter_issue(issue_data)

            data.append(issue_data)
        return data
