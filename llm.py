import json
import os
from pathlib import Path
from typing import Dict, Optional

from openai import OpenAI

from utils.file_ops import load_json_file, load_text_file


def _build_messages(master_prompt: str, inspection_text: str, thermal_text: str) -> list:
    """Compose chat messages for the OpenAI API."""
    user_content = (
        "Inspection Report Text:\n"
        f"{inspection_text}\n\n"
        "Thermal Report Text:\n"
        f"{thermal_text}\n\n"
        "Return ONLY valid JSON as per the schema."
    )
    return [
        {"role": "system", "content": master_prompt},
        {"role": "user", "content": user_content},
    ]


def _coerce_to_schema(schema: Dict, raw: Dict) -> Dict:
    """
    Lightly enforce the expected schema: fill missing keys with 'Not Available'
    and ensure list fields exist.
    """
    result = {}
    for key, default in schema.items():
        if isinstance(default, list):
            result[key] = raw.get(key) if isinstance(raw.get(key), list) else []
        elif isinstance(default, dict):
            result[key] = raw.get(key) if isinstance(raw.get(key), dict) else default
        else:
            result[key] = raw.get(key, "Not Available")
    return result


def generate_ddr_json(
    master_prompt_path: Path,
    schema_path: Path,
    extracted_data: Dict,
    model: str = "gpt-4o-mini",
    api_key: Optional[str] = None,
) -> Dict:
    """
    Call OpenAI to generate DDR JSON. Falls back to a placeholder if the call fails.
    """
    schema = load_json_file(schema_path)
    master_prompt = load_text_file(master_prompt_path)
    inspection_text = extracted_data["inspection"]["text"]
    thermal_text = extracted_data["thermal"]["text"]

    client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
    messages = _build_messages(master_prompt, inspection_text, thermal_text)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.2,
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content
        parsed = json.loads(content)
    except Exception as exc:  # broad catch to keep pipeline running
        parsed = {
            "property_issue_summary": f"LLM call failed: {exc}",
            "area_wise_observations": [],
            "probable_root_cause": "Not Available",
            "severity_assessment": {"level": "Medium", "reason": "Not Available"},
            "recommended_actions": [],
            "additional_notes": "Not Available",
            "missing_information": ["LLM generation"],
        }

    return _coerce_to_schema(schema, parsed)
