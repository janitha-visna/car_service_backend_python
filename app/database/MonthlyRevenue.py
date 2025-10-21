# database/models.py
from sqlalchemy import Column, Integer, Float
from app.database.connection import Base

class MonthlyRevenue(Base):
    __tablename__ = "monthly_revenue"

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    revenue = Column(Float, default=0.0)
