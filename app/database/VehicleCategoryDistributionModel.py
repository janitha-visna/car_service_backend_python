from sqlalchemy import Column, Integer, String
from app.database.connection import Base

class VehicleCategoryDistribution(Base):
    __tablename__ = "vehicle_category_distribution"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String(50), nullable=False)
    service_count = Column(Integer, default=0)
