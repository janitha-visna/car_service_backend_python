import pandas as pd

from app.database.VehicleCategoryDistributionModel import VehicleCategoryDistribution
from app.database.connection import SessionLocal, engine


class VehicleCategoryRepository:
    def __init__(self):
        self.table_name = VehicleCategoryDistribution.__tablename__

    def update_vehicle_distribution(self, category: str):
        # Load existing data from MySQL into a DataFrame
        try:
            df = pd.read_sql_table(self.table_name, con=engine)
        except ValueError:
            # Table empty or not existing yet
            df = pd.DataFrame(columns=["id", "category", "service_count"])

        # Check if the category exists
        if category in df["category"].values:
            df.loc[df["category"] == category, "service_count"] += 1
        else:
            # Add new row
            new_row = {"id": None, "category": category, "service_count": 1}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        # Save back to MySQL (overwrite table)
        with engine.begin() as conn:
            df.to_sql(self.table_name, con=conn, if_exists="replace", index=False)

        # Return updated category info
        updated_row = df[df["category"] == category].iloc[0].to_dict()
        return updated_row