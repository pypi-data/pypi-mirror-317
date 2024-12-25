from typing import Callable, List

from .base import BaseLLM
from .claude import Claude
from .gemini import Gemini
from .gpt import GPT

# llm can be
# claude: claude-3-5-haiku-latest, claude-3-5-sonnet-latest
# gemini: gemini-1.5-flash-latest, gemini-2.0-flash-exp, gemini-exp-1206
# gpt: gpt-4o-mini, gpt-4o-latest,o1-mini,o1


def get_llm(model: str, functions: List[Callable] = None) -> BaseLLM:
    llm = None
    if "claude" in model:
        llm = Claude(model=model)
    elif "gemini" in model:
        llm = Gemini(model=model)
    else:
        llm = GPT(model=model)
    if functions:
        for func in functions:
            llm.register_function(func)
    return llm
