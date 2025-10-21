from fastapi import APIRouter
from typing import List
from app.models.item_model import Item
from app.services.item_service import ItemService

router = APIRouter()
service = ItemService()

@router.get("/", response_model=List[Item])
def get_items():
    return service.get_items()

@router.get("/{item_id}", response_model=Item)
def get_item(item_id: int):
    return service.get_item(item_id)

@router.post("/", response_model=Item)
def create_item(item: Item):
    return service.create_item(item)

@router.put("/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    return service.update_item(item_id, updated_item)

@router.delete("/{item_id}")
def delete_item(item_id: int):
    return service.delete_item(item_id)
