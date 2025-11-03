from sqlalchemy import Column, Integer, Float, String
from app.database.connection import Base

class AverageSpendByVehicle(Base):
    __tablename__ = "average_spend_by_vehicle"

    id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_type = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    average_spend = Column(Float, default=0.0)
