from typing import List
import httpx
import json

class OllamaClient:
    """Lightweight async wrapper for Ollama generate endpoint."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    async def generate_tags(self, description: str, enums: List[str]) -> List[str]:
        prompt = f"""
                    You are a tagging assistant. Analyze the product description and return 
                    ONLY the tags from the provided list that match.

                    Description: {description}

                    Available tags: {', '.join(enums)}

                    Instructions:
                    - Return ONLY tags from the provided list above
                    - Return as a JSON array format: ["tag1", "tag2"]  
                    - Do not include any tags that are not in the provided list
                    - If no tags match, return an empty array: []

                    JSON Array:
                """
        
        payload = {
            "model": "llama3.2",
            "prompt": prompt,
            "format": "json",
            "stream": False
        }
        async with httpx.AsyncClient(timeout=15) as client:
            res = await client.post(f"{self.base_url}/api/generate", json=payload)
            res.raise_for_status()
        data = res.json()
        try:
            response_text = data.get("response", "[]")
            
            parsed = json.loads(response_text)
            
            if isinstance(parsed, list):
                tags = parsed
            elif isinstance(parsed, dict) and "tags" in parsed:
                tags = parsed["tags"]
            else:
                return []
            
            valid_tags = [tag for tag in tags if tag in enums]
            return valid_tags
            
        except (json.JSONDecodeError, KeyError, TypeError):
            return [] 