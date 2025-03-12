"""
Utility functions for My ResearchPal.
Includes text splitting and prompt saving.
"""

import os
import datetime
from enum import Enum

class ModelType(Enum):
    KNOWLEDGEABLE = "chatgpt-4o-latest"
    REASONING = "o3-mini"
    SUMMARIZING = "gpt-4o-mini"

url_separator_begin = "#####BEGINING SEPARATOR#####"
url_separator_end = "#####ENDING SEPARATOR#####"

