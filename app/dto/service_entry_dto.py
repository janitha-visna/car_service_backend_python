# dto/service_entry_dto.py
from pydantic import BaseModel
from typing import List
from datetime import date

class ServiceEntryData(BaseModel):
    number_plate: str
    vehicle_type: str
    service_types: List[str]
    amount: float
    date: date
    start_time: str
    end_time: str
    telephone_number: str
