from typing import Dict, Any, List
import boto3
import json
from .base import BaseStorage


dynamodb = boto3.resource("dynamodb")


class DynamoDBStorage(BaseStorage):
    def __init__(self, table_name: str = "Items", user_table: str = "Users"):
        self.table = dynamodb.Table(table_name)
        self.user_table = dynamodb.Table(user_table)

    def save_item(self, item_id: str, payload: Dict[str, Any]):
        self.table.put_item(Item={"id": item_id, **payload})

    def get_all_items(self) -> List[Dict[str, Any]]:
        res = self.table.scan()
        return res.get("Items", [])

    def save_user_vector(self, user_id: str, vector):
        self.user_table.put_item(Item={"id": user_id, "vector": json.dumps(vector)})

    def get_user_vector(self, user_id: str):
        res = self.user_table.get_item(Key={"id": user_id})
        item = res.get("Item")
        if item:
            return json.loads(item["vector"])
        return None 