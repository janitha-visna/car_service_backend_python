import pandas as pd
from app.dto.service_entry_dto import ServiceEntryData
from app.processors.base_processor import BaseProcessor
from app.repositories.VehicleCategoryDistributionRepository import VehicleCategoryRepository

class VehicleCategoryDistributionProcessor(BaseProcessor):
    def __init__(self):
        self.df = pd.DataFrame(columns=["vehicle_type"])
        self.repository = VehicleCategoryRepository()

    def process(self, entry: ServiceEntryData):
        # Add the vehicle type
        new_row = pd.DataFrame([{"vehicle_type": entry.vehicle_type}])
        self.df = pd.concat([self.df, new_row], ignore_index=True)

        # Group and count by vehicle type
        summary = (
            self.df.groupby("vehicle_type")
            .size()
            .reset_index(name="service_count")
        )

        # Rename for repository
        summary.rename(columns={"vehicle_type": "category"}, inplace=True)

        print("\n[VehicleCategoryDistributionProcessor] Summary:")
        print(summary)

        # Save to database
        self.repository.update_vehicle_distribution(summary)

        return summary.to_dict(orient="records")
