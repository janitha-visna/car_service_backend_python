from fastapi import FastAPI
from app.routes.item_routes import router as item_router
from app.processors.revenue_processor import RevenueProcessor
from app.coordinator.service_entry_coordinator import ServiceEntryCoordinator
from app.dto.service_entry_dto import ServiceEntryData
from app.database.connection import Base,engine
from app.processors.VehicleCategoryDistributionProcessor import VehicleCategoryDistributionProcessor
from app.config.logger import logger


# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Item API", version="1.0.0")

# Include routers
app.include_router(item_router, prefix="/items", tags=["Items"])


@app.on_event("startup")
def on_startup():
    logger.info("🚀 FastAPI application started successfully")

@app.on_event("shutdown")
def on_shutdown():
    logger.info("🛑 FastAPI application is shutting down")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000)