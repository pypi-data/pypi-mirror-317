import inspect
from functools import wraps
from typing import Any, Callable, Dict, Type, get_type_hints


def _convert_type_to_schema_type(python_type: Type) -> str:
    """Convert Python type to JSON Schema type."""
    type_map = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object",
        Any: "string",  # Default to string for Any
    }
    return type_map.get(python_type, "string")


def get_params_info(func: Callable) -> Dict[str, Dict[str, Any]]:
    """Extract parameter information from function docstring and type hints."""
    sig = inspect.signature(func)
    doc = inspect.getdoc(func) or ""
    type_hints = get_type_hints(func)

    # Initialize params_info with empty dictionaries for all parameters
    params_info = {name: {} for name in sig.parameters}
    param_lines = []
    current_param = None
    # Parse docstring to get complete parameter descriptions
    for line in doc.split("\n"):
        line = line.strip()
        if line.startswith(":param "):
            if current_param and param_lines:
                params_info[current_param]["description"] = "\n".join(param_lines)
                param_lines = []
            # Extract new parameter name and start of description
            param_part = line.split(":param ")[-1]
            current_param = param_part.split(":")[0].strip()
            description = ":".join(param_part.split(":")[1:]).strip()
            param_lines = [description]
        elif line.startswith(":return:"):
            if current_param and param_lines:
                params_info[current_param]["description"] = "\n".join(param_lines)
            break
        elif current_param and line and not line.startswith(":"):
            # Continue collecting description for current parameter
            param_lines.append(line)
    # Add the last parameter if exists
    if current_param and param_lines:
        params_info[current_param]["description"] = "\n".join(param_lines)

    # Add type information and create final parameter info
    for name, _param in sig.parameters.items():
        param_type = type_hints.get(name, Any)
        schema_type = _convert_type_to_schema_type(param_type)

        params_info[name].update(
            {
                "type": schema_type,
                "description": params_info[name].get("description", f"Parameter {name}"),
            }
        )

    return params_info


def llm_function(name: str, description: str):
    """Decorator to mark a function as available to LLM."""

    def decorator(func: Callable):
        params_info = get_params_info(func)

        # Create OpenAI/Claude/Gemini compatible schema
        schema = {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": params_info,
                "required": [
                    param_name
                    for param_name, param in inspect.signature(func).parameters.items()
                    if param.default == inspect.Parameter.empty
                ],
            },
        }

        func.llm_schema = schema

        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)

        return wrapper

    return decorator
