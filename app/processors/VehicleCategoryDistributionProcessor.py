# app/processors/VehicleCategoryDistributionProcessor.py
from app.dto.service_entry_dto import ServiceEntryData
from app.processors.base_processor import BaseProcessor
from app.repositories.VehicleCategoryDistributionRepository import VehicleCategoryRepository

class VehicleCategoryDistributionProcessor(BaseProcessor):
    def __init__(self):
        self.repository = VehicleCategoryRepository()

    def process(self, entry: ServiceEntryData):
        # Use ORM repository to update count
        result = self.repository.update_vehicle_distribution(entry.vehicle_type)
        print(f"[Processor] Updated VehicleCategoryDistribution: {result}")
        return [result]  # Return as list for consistency
