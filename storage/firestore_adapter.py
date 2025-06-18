from typing import Dict, Any, List
from google.cloud import firestore
from .base import BaseStorage


class FirestoreStorage(BaseStorage):
    def __init__(self):
        self.db = firestore.Client()
        self.items = self.db.collection("items")
        self.users = self.db.collection("users")

    def save_item(self, item_id: str, payload: Dict[str, Any]):
        self.items.document(item_id).set(payload)

    def get_all_items(self) -> List[Dict[str, Any]]:
        return [doc.to_dict() for doc in self.items.stream()]

    def save_user_vector(self, user_id: str, vector):
        self.users.document(user_id).set({"vector": vector})

    def get_user_vector(self, user_id: str):
        doc = self.users.document(user_id).get()
        return doc.to_dict()["vector"] if doc.exists else None 