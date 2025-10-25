from fastapi import FastAPI
import uvicorn  # ✅ add this import

from app.routes.item_routes import router as item_router
from app.processors.revenue_processor import RevenueProcessor
from app.coordinator.service_entry_coordinator import ServiceEntryCoordinator
from app.dto.service_entry_dto import ServiceEntryData
from app.database.connection import Base, engine

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Item API", version="1.0.0", debug=True)

# Include routers (optional if you already use them)
app.include_router(item_router)

# Initialize processors and coordinator
revenue_processor = RevenueProcessor()
coordinator = ServiceEntryCoordinator([revenue_processor])

# API endpoint
@app.post("/service-entry")
def create_service_entry(entry: ServiceEntryData):
    try:
        result = coordinator.execute(entry)
        return result
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

# ✅ This block allows PyCharm to run and debug directly
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
