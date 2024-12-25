import json
import logging
import os
from typing import AsyncIterator, Dict, List

from .base import BaseLLM

logger = logging.getLogger(__name__)


class Claude(BaseLLM):
    def __init__(
        self,
        api_keys: List[str] = None,
        base_url: str = "https://api.anthropic.com/v1",
        timeout: int = 10,
        model: str = "claude-3-5-haiku-latest",
    ):
        api_keys = api_keys or os.environ.get("ANTHROPIC_API_KEYS", "").split(",")
        if not any(api_keys):
            raise ValueError("ANTHROPIC_API_KEYS not set")
        super().__init__(api_keys, base_url, timeout, model)

    def _headers(self, model: str = "") -> Dict[str, str]:
        key = self._get_random_key()
        return {
            "Content-Type": "application/json",
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
        }

    async def chat_stream(self, messages: List[Dict[str, str]], timeout: int = 0, **kwargs) -> AsyncIterator[str]:
        data = {
            "messages": messages,
            "temperature": 0.0,
            "model": self.model,
            "stream": True,
            "max_tokens": kwargs.get("max_tokens", 4096),
        }
        if self.functions:
            data["tools"] = [
                {
                    "name": schema["name"],
                    "description": schema["description"],
                    "input_schema": schema["parameters"],
                }
                for schema in self.get_function_schemas()
            ]

        timeout = timeout or self.timeout
        data.update(kwargs)
        async with self.client.stream(
            "post",
            "messages",
            json=data,
            headers=self._headers(),
            timeout=timeout,
        ) as response:
            content = ""
            async for line in response.aiter_lines():
                if not line or line.startswith(":"):
                    continue
                if not line.startswith("data: "):
                    continue

                try:
                    chunk = json.loads(line[6:])
                    if chunk["type"] == "content_block_delta":
                        delta = chunk["delta"]["text"]
                        content += delta
                        yield delta
                except Exception:
                    if "stop_reason" in line:
                        break
                    continue

    async def chat(self, messages: List[Dict[str, str]], timeout: int = 0, **kwargs) -> str:
        data = {
            "messages": messages,
            "temperature": 0.0,
            "model": self.model,
            "max_tokens": kwargs.get("max_tokens", 4096),
        }
        if self.functions:
            # Claude API format with input_schema
            tools = []
            for schema in self.get_function_schemas():
                tools.append(
                    {
                        "name": schema["name"],
                        "description": schema["description"],
                        "input_schema": schema["parameters"],
                    }
                )
            data["tools"] = tools

        timeout = timeout or self.timeout * 3
        data.update(kwargs)
        logger.debug(f"Sending request to Claude: {json.dumps(self.format_log_data(data), indent=2)}")

        response = await self.client.post(
            "messages",
            json=data,
            headers=self._headers(),
            timeout=timeout,
        )
        response_json = response.json()
        logger.debug(f"Received response from Claude: {json.dumps(response_json, indent=2)}")

        # Handle content blocks
        if "content" in response_json and response_json["content"]:
            content_blocks = response_json["content"]
            text_response = ""

            for block in content_blocks:
                if block["type"] == "text":
                    text_response += block["text"]
                elif block["type"] == "tool_use":
                    tool_call = block
                    func_name = tool_call["name"]
                    try:
                        func_args = tool_call["input"]
                    except Exception as e:
                        return f"Error parsing tool input: {tool_call['input']} error: {str(e)}"

                    try:
                        # Call the function
                        result = await self.call_function(func_name, func_args)
                        logger.debug(f"Tool call result: {result}")
                    except Exception as e:
                        return f"Error calling tool {func_name}: {str(e)}"

                    # Add tool result to messages and call chat again
                    messages.append({"role": "assistant", "content": content_blocks})
                    messages.append(
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "tool_result",
                                    "tool_use_id": tool_call["id"],
                                    "content": json.dumps(result),
                                }
                            ],
                        }
                    )
                    logger.debug("Making recursive chat call with tool result")
                    return await self.chat(messages, timeout=timeout, **kwargs)

            return text_response

        return ""

    async def close(self):
        await self.client.aclose()
