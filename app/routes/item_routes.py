from fastapi import APIRouter
from app.processors.revenue_processor import RevenueProcessor
from app.coordinator.service_entry_coordinator import ServiceEntryCoordinator
from app.processors.VehicleCategoryDistributionProcessor import VehicleCategoryDistributionProcessor
from app.dto.service_entry_dto import ServiceEntryData
from app.config.logger import logger

router = APIRouter()


# Initialize processors and coordinator
revenue_processor = RevenueProcessor()
vehicle_category_processor = VehicleCategoryDistributionProcessor()

coordinator = ServiceEntryCoordinator([
    revenue_processor,
    vehicle_category_processor
])


@router.post("/service-entry")
def create_service_entry(entry: ServiceEntryData):
    logger.info(f"Received new service entry: {entry.number_plate}")
    result = coordinator.execute(entry)
    logger.info("Service entry processed successfully")
    return result