from typing import List, Optional
from app.models.item_model import Item

class ItemRepository:
    def __init__(self):
        self.items: List[Item] = []

    def get_all(self) -> List[Item]:
        return self.items

    def get_by_id(self, item_id: int) -> Optional[Item]:
        return next((item for item in self.items if item.id == item_id), None)

    def add(self, item: Item) -> Item:
        self.items.append(item)
        return item

    def update(self, item_id: int, updated_item: Item) -> Optional[Item]:
        for index, item in enumerate(self.items):
            if item.id == item_id:
                self.items[index] = updated_item
                return updated_item
        return None

    def delete(self, item_id: int) -> bool:
        for index, item in enumerate(self.items):
            if item.id == item_id:
                self.items.pop(index)
                return True
        return False
