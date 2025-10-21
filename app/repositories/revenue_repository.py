# app/repositories/revenue_repository.py
from app.database.MonthlyRevenue import MonthlyRevenue
from app.database.connection import SessionLocal

class RevenueRepository:
    def save_monthly_revenue(self, summary):
        db = SessionLocal()
        try:
            for _, row in summary.iterrows():
                existing = db.query(MonthlyRevenue).filter_by(
                    year=int(row["year"]), month=int(row["month"])
                ).first()
                if existing:
                    existing.revenue = float(row["amount"])
                else:
                    db.add(MonthlyRevenue(
                        year=int(row["year"]),
                        month=int(row["month"]),
                        revenue=float(row["amount"])
                    ))
            db.commit()
        finally:
            db.close()
