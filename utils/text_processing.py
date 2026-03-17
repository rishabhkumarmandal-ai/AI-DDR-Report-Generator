import re
from typing import Iterable, List


def clean_text(text: str) -> str:
    """Normalize whitespace and strip noisy characters."""
    if not text:
        return ""
    text = text.replace("\u00a0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def dedupe_lines(lines: Iterable[str]) -> List[str]:
    """Remove duplicate observations while preserving order."""
    seen = set()
    unique = []
    for line in lines:
        cleaned = line.strip()
        if cleaned and cleaned.lower() not in seen:
            unique.append(cleaned)
            seen.add(cleaned.lower())
    return unique
