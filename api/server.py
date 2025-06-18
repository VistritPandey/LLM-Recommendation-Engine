import yaml
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from tagging.ollama_client import OllamaClient
from ranking.vectorizer import to_vec
from ranking.scorer import cosine_similarity
from storage import storage_from_path


class ItemIn(BaseModel):
    id: str
    description: str


class TagIn(BaseModel):
    description: str


class RecommendIn(BaseModel):
    user_id: str


class InteractionIn(BaseModel):
    user_id: str
    item_id: str
    tags: list[str]


class ServerContext:
    def __init__(self, cfg_path=None):
        if cfg_path is None:
            cfg_path = Path(__file__).parent.parent / "config.yaml"
        cfg = yaml.safe_load(open(cfg_path))
        self.enum_list = cfg["enum_list"]
        self.storage = storage_from_path(cfg["storage_backend"])
        self.ollama = OllamaClient(cfg["model_url"])

    async def tag_description(self, description: str):
        return await self.ollama.generate_tags(description, self.enum_list)


ctx = ServerContext()
app = FastAPI(title="Recommender API")


@app.post("/tag")
async def tag_endpoint(inp: TagIn):
    tags = await ctx.tag_description(inp.description)
    return {"tags": tags}


@app.post("/item")
async def add_item_endpoint(item: ItemIn):
    tags = await ctx.tag_description(item.description)
    vec = to_vec(tags, ctx.enum_list).tolist()
    ctx.storage.save_item(item.id, {"description": item.description, "tags": tags, "vec": vec})
    return {"ok": True, "tags": tags}


@app.post("/interact")
async def interaction_endpoint(body: InteractionIn):
    prev_vec = ctx.storage.get_user_vector(body.user_id) or [0.0] * len(ctx.enum_list)
    new_vec = [a + b for a, b in zip(prev_vec, to_vec(body.tags, ctx.enum_list).tolist())]
    ctx.storage.save_user_vector(body.user_id, new_vec)
    return {"ok": True}


@app.post("/recommend")
async def recommend_endpoint(body: RecommendIn):
    user_vec = ctx.storage.get_user_vector(body.user_id)
    if user_vec is None:
        raise HTTPException(404, "user not found")
    items = ctx.storage.get_all_items()
    ranked = sorted(
        items,
        key=lambda itm: cosine_similarity(to_vec(user_vec, ctx.enum_list), to_vec(itm["tags"], ctx.enum_list)),
        reverse=True,
    )
    return {"results": ranked[:20]}


def build_app():
    return app 