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
    SUMMARIZING = "gpt-4.1-mini"

url_separator_begin = "#####BEGINING SEPARATOR#####"
url_separator_end = "#####ENDING SEPARATOR#####"

def split_into_three_sentences(text: str) -> list:
    """
    Splits the provided text into blocks where each block contains three sentences.
    A sentence is assumed to end with '.', '?' or '!'.
    """
    import re
    # Split text based on sentence ending punctuation followed by whitespace.
    sentences = re.split(r'(?<=[.!?])\s+', text)
    # Remove any empty strings and extra whitespace.
    sentences = [s.strip() for s in sentences if s.strip()]
    blocks = []
    for i in range(0, len(sentences), 3):
        block = " ".join(sentences[i:i+3])
        blocks.append(block)
    return blocks

def unique_urls(urls: list) -> list:
    """
    Flattens and Removes duplicate URLs from the provided list of list of urls.
    """
    unique_ruls = set()
    for url_list in urls:
        unique_ruls.update(url_list)
    return list(unique_ruls)