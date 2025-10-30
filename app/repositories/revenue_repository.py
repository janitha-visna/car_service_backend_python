# app/repositories/revenue_repository.py
from app.config.logger import logger
from app.models.MonthlyRevenueModel import MonthlyRevenue
from app.database.connection import SessionLocal
from app.config.logger import repository_logger
from app.repositories.base_repository import BaseRepository

class RevenueRepository(BaseRepository):
    def save_monthly_revenue(self, summary):

        repository_logger.info("Starting to save monthly revenue data...")
        try:
            for _, row in summary.iterrows():
                existing = self.db.query(MonthlyRevenue).filter_by(
                    year=int(row["year"]), month=int(row["month"])
                ).first()
                if existing:
                    repository_logger.debug(f"Updating revenue for {row['year']}-{row['month']}")
                    existing.revenue = float(row["amount"])
                else:
                    repository_logger.debug(f"Inserting new revenue for {row['year']}-{row['month']}")
                    self.db.add(MonthlyRevenue(
                        year=int(row["year"]),
                        month=int(row["month"]),
                        revenue=float(row["amount"])
                    ))

            logger.info("Monthly revenue saved successfully ✅")
        except Exception as e:
            repository_logger.exception(f"Error while saving monthly revenue: {e}")
        finally:

            repository_logger.debug("Database session closed.")

