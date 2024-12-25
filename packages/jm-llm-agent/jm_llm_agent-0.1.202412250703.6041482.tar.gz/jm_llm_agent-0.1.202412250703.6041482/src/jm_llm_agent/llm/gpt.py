import json
import logging
import os
from typing import Any, AsyncIterator, Dict, List

from .base import BaseLLM

logger = logging.getLogger(__name__)


class GPT(BaseLLM):
    def __init__(
        self,
        api_keys: List[str] = None,
        base_url: str = "https://api.openai.com/v1",
        timeout: int = 20,
        model: str = "gpt-4o-mini",
    ):
        api_keys = api_keys or os.environ.get("OPENAI_API_KEYS", "").split(",")
        if not any(api_keys):
            raise ValueError("OPENAI_API_KEYS not set")
        super().__init__(api_keys, base_url, timeout, model)

    def _headers(self, model: str = "") -> Dict[str, str]:
        key = self._get_random_key()
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",
        }

    async def moderation(self, prompt: str, timeout: int = 0) -> Dict[str, Any]:
        data = {"input": prompt}
        response = await self.client.post(
            "moderations",
            headers=self._headers(),
            json=data,
            timeout=timeout or self.client.timeout,
        )
        return response.json()

    async def gen_image(self, prompt: str, size: str = "1024x1024", n: int = 1, timeout: int = 60) -> Dict[str, Any]:
        data = {"prompt": prompt, "n": n, "size": size, "model": "dall-e-3"}
        response = await self.client.post(
            "images/generations",
            headers=self._headers(),
            json=data,
            timeout=timeout or self.client.timeout,
        )
        return response.json()

    async def chat_stream(self, messages: List[Dict[str, str]], timeout: int = 0, **kwargs) -> AsyncIterator[str]:
        data = {
            "messages": messages,
            "model": self.model,
            "temperature": 0.0,
            "stream": True,
        }
        if self.functions:
            data["functions"] = self.get_function_schemas()
            data["function_call"] = "auto"

        timeout = timeout or self.timeout
        data.update(kwargs)

        async with self.client.stream(
            "post",
            "chat/completions",
            headers=self._headers(model=data["model"]),
            json=data,
            timeout=timeout,
        ) as response:
            async for line in response.aiter_lines():
                if not line or line.startswith("data: [DONE]"):
                    continue
                if not line.startswith("data: "):
                    continue
                try:
                    chunk = json.loads(line[6:])
                    if (
                        "choices" in chunk
                        and len(chunk["choices"]) > 0
                        and "delta" in chunk["choices"][0]
                        and "content" in chunk["choices"][0]["delta"]
                    ):
                        yield chunk["choices"][0]["delta"]["content"]
                except Exception as e:
                    logger.error(f"Error parsing chunk: {e}")
                    continue

    async def chat(self, messages: List[Dict[str, str]], detail: bool = False, **kwargs) -> str:
        data = {"messages": messages, "model": self.model, "temperature": 0.0}
        if self.functions:
            data["functions"] = self.get_function_schemas()
            data["function_call"] = "auto"

        timeout = self.timeout * 3
        if "timeout" in kwargs:
            timeout = kwargs["timeout"]
            kwargs.pop("timeout")
        data.update(kwargs)
        debug_data = self.format_log_data(data)
        logger.debug(f"Sending request to GPT: {json.dumps(debug_data, indent=2)}")
        response = await self.client.post(
            "chat/completions",
            headers=self._headers(model=data["model"]),
            json=data,
            timeout=timeout,
        )
        res = response.json()
        logger.debug(f"Received response from GPT: {json.dumps(res, indent=2)}")
        # Handle function calls
        if not detail and "choices" in res and len(res["choices"]) > 0:
            message = res["choices"][0]["message"]
            if message.get("function_call"):
                func_call = message["function_call"]
                func_name = func_call["name"]
                try:
                    func_args = json.loads(func_call["arguments"])
                except json.JSONDecodeError:
                    # If arguments are malformed, return the error message
                    return f"Error parsing function arguments: {func_call['arguments']}"

                try:
                    # Call the function
                    result = await self.call_function(func_name, func_args)
                except Exception as e:
                    # If function call fails, return the error message
                    return f"Error calling function {func_name}: {str(e)}"

                # Add function result to messages and call chat again
                messages.append(
                    {
                        "role": "assistant",
                        "content": None,
                        "function_call": {
                            "name": func_name,
                            "arguments": func_call["arguments"],
                        },
                    }
                )
                messages.append(
                    {
                        "role": "function",
                        "name": func_name,
                        "content": json.dumps(result),
                    }
                )
                return await self.chat(messages, detail=detail, **kwargs)

            return message.get("content", "")

        return res if detail else res["choices"][0]["message"].get("content", "")
