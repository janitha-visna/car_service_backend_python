
import pandas as pd

from app.database.MonthlyRevenue import MonthlyRevenue
from app.dto.service_entry_dto import ServiceEntryData
from app.processors.base_processor import BaseProcessor
from sqlalchemy.exc import SQLAlchemyError
from app.database.connection import SessionLocal


class RevenueProcessor(BaseProcessor):
    def __init__(self):
        self.df = pd.DataFrame(columns=[
            "date", "amount"
        ])

    def process(self, entry: ServiceEntryData):
        # Add new record to DataFrame
        new_row = pd.DataFrame([{
            "date": entry.date,
            "amount": entry.amount
        }])
        self.df = pd.concat([self.df, new_row], ignore_index=True)

        # Extract year and month for grouping
        self.df["year"] = pd.to_datetime(self.df["date"]).dt.year
        self.df["month"] = pd.to_datetime(self.df["date"]).dt.month

        # Group by year and month, calculate revenue
        revenue_summary = (
            self.df.groupby(["year", "month"])["amount"]
            .sum()
            .reset_index()
        )

        print("\n[RevenueProcessor] Revenue Summary:")
        print(revenue_summary)

        # Save to MySQL
        db = SessionLocal()
        try:
            for _, row in revenue_summary.iterrows():
                existing = (
                    db.query(MonthlyRevenue)
                    .filter_by(year=int(row["year"]), month=int(row["month"]))
                    .first()
                )

                if existing:
                    existing.revenue = float(row["amount"])
                else:
                    new_entry = MonthlyRevenue(
                        year=int(row["year"]),
                        month=int(row["month"]),
                        revenue=float(row["amount"])
                    )
                    db.add(new_entry)

            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            print("[DB Error]", e)
            raise
        finally:
            db.close()

        return {
            "revenue_summary": revenue_summary.to_dict(orient="records")
        }
