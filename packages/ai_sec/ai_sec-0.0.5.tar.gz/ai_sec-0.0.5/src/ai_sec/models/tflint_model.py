import json
import logging
from typing import Any, List, Optional

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class TFLintRange(BaseModel):
    filename: str
    start: dict
    end: dict


class TFLintRule(BaseModel):
    name: str
    severity: str
    link: Optional[str] = None  # Link to the rule documentation


class TFLintIssue(BaseModel):
    rule: TFLintRule
    message: str
    range: TFLintRange
    callers: Optional[List[Any]] = []

    def get_file_path(self):
        """Return the file path directly as provided in the JSON."""
        return self.range.filename


class TFLintResult(BaseModel):
    issues: List[TFLintIssue] = []
    errors: List[Any] = []

    @classmethod
    def from_raw_json(cls, raw_json):
        """
        Factory method to create a TFLintResult object from raw JSON or dict.

        :param raw_json: The raw JSON output from TFLint (either a string or a dict).
        :return: Parsed TFLintResult object.
        """
        try:
            # If raw_json is a string, parse it, else use it directly
            if isinstance(raw_json, str):
                parsed_json = json.loads(raw_json)
            else:
                parsed_json = raw_json  # It's already a dict, so use it directly
            return cls.parse_obj(parsed_json)
        except Exception as e:
            logger.error(f"Error parsing TFLint JSON: {e}")
            raise ValueError(f"Invalid TFLint result format: {e}")
