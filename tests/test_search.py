
from googlesearch import search
import json
import os
import sys
import asyncio  # Added to enable async execution

# Add the project root directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from src.config import SEARCH_PER_SERP
from src.ai import get_ai_responses
from src.utils import ModelType 


x = search("What is the capital of France?", num_results=1, unique=True, region="us")

for i in x:
    print(i)


xx="""
# Art and Humanity Meets Science: The Creative Side of STEM

## Table of Contents
1. Introduction
2. Literature Review
3."""

print(xx)
print("=========")
print(xx.strip())