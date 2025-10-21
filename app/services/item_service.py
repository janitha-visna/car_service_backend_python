from fastapi import HTTPException
from app.models.item_model import Item
from app.repositories.item_repository import ItemRepository

class ItemService:
    def __init__(self):
        self.repo = ItemRepository()

    def get_items(self):
        return self.repo.get_all()

    def get_item(self, item_id: int):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item

    def create_item(self, item: Item):
        return self.repo.add(item)

    def update_item(self, item_id: int, updated_item: Item):
        item = self.repo.update(item_id, updated_item)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item

    def delete_item(self, item_id: int):
        if not self.repo.delete(item_id):
            raise HTTPException(status_code=404, detail="Item not found")
        return {"message": "Item deleted successfully"}
