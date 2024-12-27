import json
import logging
from typing import Any, List

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class TFSecLocation(BaseModel):
    filename: str
    start_line: int
    end_line: int


class TFSecResult(BaseModel):
    rule_id: str
    rule_description: str
    severity: str
    resource: str
    location: TFSecLocation
    links: List[str] = []  # Links are already provided as a list of URLs in the JSON

    def get_file_path(self, base_directory):
        """Return the file path, relative to the base directory."""
        abs_path = self.location.filename
        return abs_path.replace(base_directory, "").lstrip("/")


class TFSecReport(BaseModel):
    results: List[Any] = []

    @classmethod
    def from_raw_json(cls, raw_json):
        """
        Factory method to create a TFSecReport object from raw JSON or dict.

        :param raw_json: The raw JSON output from TFSec (either a string or a dict).
        :return: Parsed TFSecReport object.
        """
        try:
            # If raw_json is a string, parse it, else use it directly
            if isinstance(raw_json, str):
                parsed_json = json.loads(raw_json)
            else:
                parsed_json = raw_json  # It's already a dict, so use it directly
            return cls.parse_obj(parsed_json)
        except Exception as e:
            logger.error(f"Error parsing TFSec JSON: {e}")
            raise ValueError(f"Invalid TFSec result format: {e}")
