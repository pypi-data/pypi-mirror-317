import logging
import os
import random
from abc import ABC, abstractmethod
from typing import Any, AsyncIterator, Callable, Dict, List

import httpx

logger = logging.getLogger(__name__)


class BaseLLM(ABC):
    def __init__(
        self,
        api_keys: List[str],
        base_url: str = "",
        timeout: int = 10,
        model: str = "",
    ):
        self.api_keys = api_keys
        self.base_url = base_url
        self.model = model
        self.timeout = timeout
        proxy = os.getenv("PROXY")
        self.client = httpx.AsyncClient(base_url=base_url, proxy=proxy, timeout=timeout)
        self.functions: Dict[str, Dict[str, Any]] = {}

    def _get_random_key(self) -> str:
        return self.api_keys[random.randint(0, len(self.api_keys) - 1)]

    def _truncate_content(self, content: any, max_length: int = 100) -> str:
        if not isinstance(content, str):
            return content
        if not content or len(content) <= max_length * 2:
            return content
        return f"{content[:max_length]}...{content[-max_length:]}"

    def format_log_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if isinstance(data, str):
            return self._truncate_content(data)
        if isinstance(data, list):
            return [self.format_log_data(item) for item in data]
        formatted = {}
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str):
                    formatted[key] = self._truncate_content(value)
                elif isinstance(value, dict):
                    formatted[key] = self.format_log_data(value)
                elif isinstance(value, list):
                    formatted[key] = [self.format_log_data(item) for item in value]
                else:
                    formatted[key] = value
        return formatted

    @abstractmethod
    def _headers(self, model: str = "") -> Dict[str, str]:
        """Return headers required for API calls"""
        pass

    def register_function(self, func: Callable):
        """Register a function to be available to the LLM."""
        if not hasattr(func, "llm_schema"):
            raise ValueError(f"Function {func.__name__} is not decorated with @llm_function")

        self.functions[func.llm_schema["name"]] = {
            "schema": func.llm_schema,
            "callable": func,
        }

    def get_function_schemas(self) -> List[Dict[str, Any]]:
        """Get function schemas in format required by specific LLM."""
        return [f["schema"] for f in self.functions.values()]

    async def call_function(self, name: str, arguments: Dict[str, Any]) -> Any:
        """Call a registered function with given arguments."""
        if name not in self.functions:
            raise ValueError(f"Function {name} not found")

        func = self.functions[name]["callable"]
        return await func(**arguments)

    @abstractmethod
    async def chat_stream(self, messages: List[Dict[str, str]], timeout: int = 0, **kwargs) -> AsyncIterator[str]:
        """Stream chat completion responses"""
        pass

    @abstractmethod
    async def chat(self, messages: List[Dict[str, str]], timeout: int = 0, **kwargs) -> str:
        """Get chat completion response"""
        pass

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
