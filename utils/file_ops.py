import json
from pathlib import Path
from typing import Any


def ensure_dir(path: Path) -> Path:
    """Create directory if it doesn't exist and return the Path."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_text_file(path: Path) -> str:
    """Read a text file safely."""
    return path.read_text(encoding="utf-8")


def load_json_file(path: Path) -> Any:
    """Load JSON content from a file."""
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def dump_json_file(path: Path, data: Any) -> None:
    """Write JSON content to a file with indentation."""
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
