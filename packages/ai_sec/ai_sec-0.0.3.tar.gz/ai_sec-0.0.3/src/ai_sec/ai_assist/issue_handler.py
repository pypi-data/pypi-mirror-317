import hashlib
import json
import logging
import os
from typing import Dict, Optional

import openai
from openai.error import (
    APIConnectionError,
    AuthenticationError,
    InvalidRequestError,
    OpenAIError,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

CACHE_FILE = os.path.expanduser("~/.ai_sec/openai_cache.json")


class AIHandlerFactory:
    _instance = None

    @staticmethod
    def get_handler() -> "IssueHandler":
        """Retrieve or create the IssueHandler instance."""
        if AIHandlerFactory._instance is None:
            AIHandlerFactory._instance = IssueHandler()
        return AIHandlerFactory._instance


class IssueHandler:
    def __init__(self, model="gpt-4", timeout=30):
        self.model = model
        self.timeout = timeout
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key:
            openai.api_key = self.api_key
        else:
            raise RuntimeError(
                "OpenAI API key not set. Please set the API key to use this feature."
            )

        # Load cache if it exists, otherwise create an empty dictionary
        self.cache = self.load_cache()

    def load_cache(self) -> Dict[str, str]:
        """Load cache from a JSON file if it exists, otherwise return an empty dictionary."""
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r") as cache_file:
                data = json.load(cache_file)
                if isinstance(data, dict):
                    return {str(k): str(v) for k, v in data.items()}
        return {}

    def save_cache(self) -> None:
        """Save the cache to a file."""
        with open(CACHE_FILE, "w") as cache_file:
            json.dump(self.cache, cache_file)

    def get_cache_key(self, prompt: str) -> str:
        """Generate a cache key by hashing the prompt."""
        return hashlib.sha256(prompt.encode("utf-8")).hexdigest()

    def get_openai_response(self, prompt: str) -> Optional[str]:
        """Fetch a response from OpenAI, using cache if available."""
        cache_key = self.get_cache_key(prompt)

        # Check if the response is already cached
        if cache_key in self.cache:
            logger.info("Using cached response for prompt.")
            return self.cache.get(cache_key)  # type: ignore

        # If not cached, fetch the response from OpenAI
        try:
            completion = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert in security and best practices for infrastructure.",
                    },
                    {"role": "user", "content": prompt},
                ],
                timeout=self.timeout,
            )
            response: str = completion.choices[0].message["content"].strip()

            if not response:
                logger.error("Received an invalid or empty response from OpenAI.")
                return None

            # Cache the response and save the cache
            self.cache[cache_key] = response
            self.save_cache()

            return response
        except (
            AuthenticationError,
            APIConnectionError,
            InvalidRequestError,
            OpenAIError,
        ) as e:
            logger.error(f"OpenAI error: {e}")
            raise RuntimeError(f"OpenAI error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise RuntimeError(f"Unexpected error: {e}")

    def infer_severity(self, description: str, framework: str) -> str:
        """Determine the severity based on the issue description."""
        prompt = (
            f"Based on the following issue in the {framework} framework: '{description}', "
            "please determine the severity of the issue. Respond ONLY with one of the following: "
            "CRITICAL, HIGH, MEDIUM, LOW. Do not provide any other text."
        )
        response = self.get_openai_response(prompt)
        valid_severities = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]

        if response and response.upper().strip() in valid_severities:
            return response.upper().strip()
        logger.error(f"Unable to determine severity for the issue: {description}")
        return "UNKNOWN"

    def generate_resolution_context(self, description: str, framework: str) -> str:
        """Generate additional context for CRITICAL or HIGH severity issues."""
        prompt = (
            f"Given the following high-severity issue in the {framework} framework: '{description}', "
            "provide a short explanation of the issue and recommended resolution in one paragraph. Do not include the words 'Summary' or 'Resolution'."
        )
        response = self.get_openai_response(prompt)
        return response or "No additional context available."

    def process_issue(
        self, description: str, framework: str
    ) -> Dict[str, Optional[str]]:
        """Process the issue description, return severity, and optionally provide resolution context."""
        result: Dict[str, Optional[str]] = {"severity": None, "context": None}

        try:
            severity = self.infer_severity(description, framework)
            result["severity"] = severity

            if severity in ["CRITICAL", "HIGH"]:
                context = self.generate_resolution_context(description, framework)
                result["context"] = context

            return result
        except RuntimeError as e:
            logger.error(f"Error processing issue: {e}")
            return result
