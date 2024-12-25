"""
LLM client package providing unified interface for Claude, GPT, and Gemini.
"""

from dotenv import load_dotenv

from .base import BaseLLM
from .claude import Claude
from .gemini import Gemini
from .gpt import GPT
from .llm import get_llm

# Load environment variables at package initialization
load_dotenv()

__all__ = ["BaseLLM", "Claude", "Gemini", "GPT", "get_llm"]
