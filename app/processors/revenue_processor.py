
import pandas as pd

from app.dto.service_entry_dto import ServiceEntryData
from app.processors.base_processor import BaseProcessor
from app.repositories.revenue_repository import RevenueRepository
from app.config.logger import logger




class RevenueProcessor(BaseProcessor):
    def __init__(self):
        self.df = pd.DataFrame(columns=[
            "date", "amount"
        ])
        self.repository = RevenueRepository()

    def process(self, entry: ServiceEntryData):
        # Add new record to DataFrame
        new_row = pd.DataFrame([{
            "date": entry.date,
            "amount": entry.amount
        }])
        self.df = pd.concat([self.df, new_row], ignore_index=True)
        logger.info(f"DataFrame after concat:\n{self.df.to_string()}")


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
        logger.info("Revenue summary:\n%s", revenue_summary.to_string(index=False))

        self.repository.save_monthly_revenue(revenue_summary)
        return revenue_summary.to_dict(orient="records")


