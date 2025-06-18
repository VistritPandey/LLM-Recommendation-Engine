import asyncio
from tagging.ollama_client import OllamaClient


def test_generate_tags(monkeypatch):
    async def fake_generate(self, description, enums):
        return [enums[0]]

    monkeypatch.setattr(OllamaClient, "generate_tags", fake_generate)
    client = OllamaClient("http://fake")
    tags = asyncio.run(client.generate_tags("desc", ["a", "b"]))
    assert tags == ["a"] 