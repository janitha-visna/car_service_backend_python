import pandas as pd
from app.dto.service_entry_dto import ServiceEntryData
from app.processors.base_processor import BaseProcessor
from app.repositories.AverageSpendByVehicleRepository import AverageSpendByVehicleRepository
from app.config.logger import logger

class AverageSpendByVehicleProcessor(BaseProcessor):
    def __init__(self):
        self.df = pd.DataFrame(columns=[
            "vehicle_type", "date", "amount"
        ])
        self.repository = AverageSpendByVehicleRepository()

    def process(self, entry: ServiceEntryData):
        # Add new entry
        new_row = pd.DataFrame([{
            "vehicle_type": entry.vehicle_type,
            "date": entry.date,
            "amount": entry.amount
        }])
        self.df = pd.concat([self.df, new_row], ignore_index=True)
        logger.info(f"Updated AverageSpend DataFrame:\n{self.df.to_string(index=False)}")

        # Add year and month
        self.df["year"] = pd.to_datetime(self.df["date"]).dt.year
        self.df["month"] = pd.to_datetime(self.df["date"]).dt.month

        # Group by vehicle type, year, and month to calculate average
        avg_summary = (
            self.df.groupby(["vehicle_type", "year", "month"])["amount"]
            .mean()
            .reset_index()
            .rename(columns={"amount": "average_spend"})
        )

        logger.info("Monthly Average Spend Summary:\n%s", avg_summary.to_string(index=False))

        # Save to DB
        self.repository.save_average_spend(avg_summary)

        return avg_summary.to_dict(orient="records")
