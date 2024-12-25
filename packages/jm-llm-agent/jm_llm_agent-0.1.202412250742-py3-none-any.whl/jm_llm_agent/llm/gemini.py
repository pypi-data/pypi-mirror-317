import json
import logging
import os
from typing import Any, AsyncIterator, Dict, List

from .base import BaseLLM

logger = logging.getLogger(__name__)


class Gemini(BaseLLM):
    def __init__(
        self,
        api_keys: List[str] = None,
        base_url: str = "https://generativelanguage.googleapis.com/v1beta",
        timeout: int = 20,
        model: str = "gemini-2.0-flash-exp",
    ):
        api_keys = api_keys or os.environ.get("GEMINI_API_KEYS", "").split(",")
        if not any(api_keys):
            raise ValueError("GEMINI_API_KEYS not set")
        super().__init__(api_keys, base_url, timeout, model)

    def _headers(self, model: str = "") -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
        }

    def _convert_messages(self, messages: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        # Convert chat format from OpenAI style to Gemini format
        contents = []
        for msg in messages:
            role = msg["role"]
            if role == "system":
                # Prepend system message to first user message
                continue
            content = msg["content"]

            if role == "user":
                contents.append({"role": "user", "parts": [{"text": content}]})
            elif role == "assistant":
                contents.append({"role": "model", "parts": [{"text": content}]})
            elif role == "function":
                contents.append(
                    {
                        "role": "user",
                        "parts": [
                            {
                                "functionResponse": {
                                    "name": msg["name"],
                                    "response": content,
                                }
                            }
                        ],
                    }
                )
            elif role == "gemini":
                contents.append({"role": "model", "parts": content})
        return contents

    async def chat_stream(self, messages: List[Dict[str, str]], timeout: int = 0, **kwargs) -> AsyncIterator[str]:
        contents = self._convert_messages(messages)
        data = {
            "contents": contents,
            "model": self.model,
            "safety_settings": kwargs.get("safety_settings", []),
            "generation_config": {
                "temperature": kwargs.get("temperature", 0),
                "top_p": kwargs.get("top_p", 0.8),
                "top_k": kwargs.get("top_k", 1),
                "max_output_tokens": kwargs.get("max_tokens", 4096),
            },
        }
        if self.functions:
            function_declarations = self.get_function_schemas()
            data["tools"] = [{"function_declarations": function_declarations}]

        timeout = timeout or self.timeout
        data.update(kwargs)

        key = self._get_random_key()
        url = f"models/{self.model}:streamGenerateContent?alt=sse&key={key}"
        # logger.debug(f"Sending request to Gemini: {json.dumps(data, indent=2)}")
        async with self.client.stream(
            "post",
            url,
            json=data,
            headers=self._headers(),
            timeout=timeout,
        ) as response:
            async for line in response.aiter_lines():
                if not line or not line.startswith("data: "):
                    continue
                try:
                    chunk = json.loads(line[6:])
                    if "candidates" in chunk and chunk["candidates"]:
                        candidate = chunk["candidates"][0]
                        if "content" in candidate and "parts" in candidate["content"]:
                            for part in candidate["content"]["parts"]:
                                if "text" in part:
                                    delta = part["text"]
                                    yield delta
                except Exception:
                    continue

    async def chat(self, messages: List[Dict[str, str]], timeout: int = 0, **kwargs) -> str:
        contents = self._convert_messages(messages)
        data = {
            "contents": contents,
            "model": self.model,
            "safety_settings": kwargs.get("safety_settings", []),
            "generation_config": {
                "temperature": kwargs.get("temperature", 0),
                "top_p": kwargs.get("top_p", 0.8),
                "top_k": kwargs.get("top_k", 1),
                "max_output_tokens": kwargs.get("max_tokens", 4096),
            },
        }
        if self.functions:
            function_declarations = self.get_function_schemas()
            data["tools"] = [{"function_declarations": function_declarations}]

        timeout = timeout or self.timeout * 3
        data.update(kwargs)
        logger.debug(f"Sending request to Gemini: {json.dumps(self.format_log_data(data), indent=2)}")

        response = await self.client.post(
            f"models/{self.model}:generateContent",
            json=data,
            headers=self._headers(),
            timeout=timeout,
            params={"key": self._get_random_key()},
        )
        response_json = response.json()
        logger.debug(f"Received response from Gemini: {json.dumps(response_json, indent=2)}")

        if "candidates" in response_json and response_json["candidates"]:
            candidate = response_json["candidates"][0]

            if "content" in candidate:
                content = candidate["content"]
                if content.get("parts"):
                    text_response = ""
                    for part in content["parts"]:
                        if part.get("text"):
                            text_response += part["text"]
                        elif part.get("functionCall"):
                            func_call = part["functionCall"]
                            func_name = func_call["name"]
                            try:
                                func_args = func_call["args"]
                            except json.JSONDecodeError as e:
                                logger.error(f"Failed to parse function arguments: {e}")
                                return f"Error parsing function arguments: {func_call}"

                            try:
                                # Call the function
                                result = await self.call_function(func_name, func_args)
                            except Exception as e:
                                return f"Error calling function {func_name}: {str(e)}"

                            # Add function result to messages
                            messages.append({"role": "gemini", "content": [part]})
                            messages.append(
                                {
                                    "role": "function",
                                    "name": func_name,
                                    "content": {"content": result},
                                }
                            )

                    # After processing all parts, make a recursive call if any function was called
                    if any(part.get("functionCall") for part in content["parts"]):
                        logger.debug("Making recursive chat call with function results")
                        return await self.chat(messages, timeout=timeout, **kwargs)

                    return text_response
        return ""

    async def close(self):
        await self.client.aclose()
