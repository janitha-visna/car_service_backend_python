# app/repositories/revenue_repository.py
from app.config.logger import logger
from app.database.MonthlyRevenue import MonthlyRevenue
from app.database.connection import SessionLocal

class RevenueRepository:
    def save_monthly_revenue(self, summary):
        db = SessionLocal()
        logger.info("Starting to save monthly revenue data...")
        try:
            for _, row in summary.iterrows():
                existing = db.query(MonthlyRevenue).filter_by(
                    year=int(row["year"]), month=int(row["month"])
                ).first()
                if existing:
                    logger.debug(f"Updating revenue for {row['year']}-{row['month']}")
                    existing.revenue = float(row["amount"])
                else:
                    logger.debug(f"Inserting new revenue for {row['year']}-{row['month']}")
                    db.add(MonthlyRevenue(
                        year=int(row["year"]),
                        month=int(row["month"]),
                        revenue=float(row["amount"])
                    ))
            db.commit()
            logger.info("Monthly revenue saved successfully ✅")
        except Exception as e:
            logger.exception(f"Error while saving monthly revenue: {e}")
        finally:
            db.close()
            logger.debug("Database session closed.")
