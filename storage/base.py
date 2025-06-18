from abc import ABC, abstractmethod
from typing import Dict, Any, List


class BaseStorage(ABC):
    """Common interface for any backend."""

    @abstractmethod
    def save_item(self, item_id: str, payload: Dict[str, Any]):
        raise NotImplementedError

    @abstractmethod
    def get_all_items(self) -> List[Dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def save_user_vector(self, user_id: str, vector: List[float]):
        raise NotImplementedError

    @abstractmethod
    def get_user_vector(self, user_id: str) -> List[float] | None:
        raise NotImplementedError 