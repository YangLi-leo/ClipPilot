"""
Text Processing Utilities for ClipPilot.

This module provides utilities for processing and analyzing text.
"""

import logging
import re

logger = logging.getLogger(__name__)


def clean_transcript(transcript):
    """
    Clean a transcript by removing unnecessary characters and formatting.

    Args:
        transcript (str): The raw transcript text

    Returns:
        str: The cleaned transcript
    """
    cleaned = re.sub(r"\[\d+:\d+:\d+\]", "", transcript)

    cleaned = re.sub(r"^\s*\w+\s*:", "", cleaned, flags=re.MULTILINE)

    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    return cleaned


def split_into_chunks(text, chunk_size=1000):
    """
    Split text into chunks of approximately equal size.

    Args:
        text (str): The text to split
        chunk_size (int): The approximate size of each chunk

    Returns:
        list: A list of text chunks
    """
    sentences = re.split(r"(?<=[.!?])\s+", text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= chunk_size:
            current_chunk += sentence + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def extract_keywords(text, max_keywords=10):
    """
    Extract important keywords from text.

    Args:
        text (str): The text to analyze
        max_keywords (int): Maximum number of keywords to extract

    Returns:
        list: A list of keywords
    """

    words = re.findall(r"\b\w+\b", text.lower())

    word_counts = {}
    for word in words:
        if len(word) > 3:  # Ignore short words
            word_counts[word] = word_counts.get(word, 0) + 1

    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

    return [word for word, count in sorted_words[:max_keywords]]
