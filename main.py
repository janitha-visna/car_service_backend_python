from fastapi import FastAPI
from app.routes.item_routes import router as item_router
from app.processors.revenue_processor import RevenueProcessor
from app.coordinator.service_entry_coordinator import ServiceEntryCoordinator
from app.dto.service_entry_dto import ServiceEntryData
from app.database.connection import Base,engine


# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Item API", version="1.0.0")



revenue_processor = RevenueProcessor()

coordinator = ServiceEntryCoordinator([
    revenue_processor
])

@app.post("/service-entry")
def create_service_entry(entry: ServiceEntryData):
    result = coordinator.execute(entry)
    return result