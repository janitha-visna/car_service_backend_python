# app/models/FailedServiceEntryModel.py
from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.sql import func
from app.database.connection import Base

class FailedServiceEntry(Base):
    __tablename__ = "failed_service_entries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    number_plate = Column(String(20), nullable=False)
    vehicle_type = Column(String(50), nullable=True)
    amount = Column(Float, nullable=True)
    service_types = Column(Text, nullable=True)  # Store as JSON string
    error_message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())