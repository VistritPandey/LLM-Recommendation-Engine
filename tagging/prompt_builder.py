from typing import List, Dict, Any


def build_prompt(description: str, enums: List[str]) -> Dict[str, Any]:
    return {
        "description": description,
        "enums": enums,
        "task": "return json array of enums that match",
    } 