import re
from emoji import demojize


def clean_text(text):
    """Preprocess text for emotion analysis"""
    # Convert emojis to text descriptions
    text = demojize(text, delimiters=(" ", " "))

    # Remove special characters except basic punctuation
    text = re.sub(r"[^a-zA-Z0-9.!?, ]", " ", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text.lower()

def handle_special_characters(text: str) -> str:
    # Handle ellipsis and repeated punctuation
    text = re.sub(r"\.{3,}", "…", text)
    text = re.sub(r"!{2,}", "!", text)
    text = re.sub(r"\?{2,}", "?", text)
    return text