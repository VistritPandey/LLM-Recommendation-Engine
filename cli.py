import asyncio
import json
import sys
import yaml
from pathlib import Path

from tagging.ollama_client import OllamaClient


async def main():
    if len(sys.argv) < 2:
        print("usage: python -m cli 'description here'")
        sys.exit(1)
    description = sys.argv[1]
    config_path = Path(__file__).parent / "config.yaml"
    cfg = yaml.safe_load(open(config_path))
    client = OllamaClient(cfg["model_url"])
    tags = await client.generate_tags(description, cfg["enum_list"])
    print(json.dumps({"tags": tags}, indent=2))


if __name__ == "__main__":
    asyncio.run(main()) 