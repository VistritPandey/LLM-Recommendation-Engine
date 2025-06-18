# Recommender Engine

An open source recommendation service that converts any text image or video description into clean tags with a local LLM then serves personalized results using light vector math. Copy paste into your stack and chill.

## Why you want it

* Universal Works for products posts clips bios anything described in words
* Bring your own tags Define enums in YAML and you are set
* Local friendly Runs with Ollama meaning your data never leaves your box
* Pluggable storage SQLite for hack nights Firestore or DynamoDB for prod
* Fully typed FastAPI endpoints plus a CLI for quick experiments

## Fast track

```bash
poetry install
poetry run uvicorn api.server:app --reload
```

Swagger UI pops up at http://127.0.0.1:8000/docs

* POST /tag get tags for a description
* POST /item store an item with tags and vector
* POST /interact update a user profile after a click view or like
* POST /recommend grab the top matches for that user

## Requirements

* Python 3.10 or newer
* Ollama running with your fave model

```bash
ollama pull llama3
ollama serve
```

## Config

Edit `config.yaml`

* `model_url` points at Ollama
* `storage_backend` selects your adapter
* `enum_list` lists valid tags

Switch backend by setting `storage_backend` to one of

* `storage.sqlite_adapter.SQLiteStorage`
* `storage.firestore_adapter.FirestoreStorage`
* `storage.dynamodb_adapter.DynamoDBStorage`

## Cloud notes

Firestore

```bash
export GOOGLE_APPLICATION_CREDENTIALS=your-key.json
```

DynamoDB

```bash
aws configure
```

## CLI vibe

```bash
poetry run python -m cli "A 4K sixty Hz monitor with ultra thin bezels"
```

## Tests

```bash
poetry run pytest -q
```

Ship it and have fun. 