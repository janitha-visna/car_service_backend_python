import pandas as pd
from app.database.VehicleCategoryDistributionModel import VehicleCategoryDistribution
from app.database.connection import engine

class VehicleCategoryRepository:
    def __init__(self):
        self.table_name = VehicleCategoryDistribution.__tablename__

    def update_vehicle_distribution(self, summary: pd.DataFrame):
        print("\n[VehicleCategoryRepository] Received summary:")
        print(summary)

        # Load existing data from MySQL into a DataFrame
        try:
            df = pd.read_sql_table(self.table_name, con=engine)
            print(f"[VehicleCategoryRepository] Existing table data:\n{df}")
        except ValueError:
            print("[VehicleCategoryRepository] Table empty or does not exist yet.")
            df = pd.DataFrame(columns=["category", "service_count"])

        # Iterate over summary rows
        for _, row in summary.iterrows():
            category = row["category"]
            count = row["service_count"]

            if category in df["category"].values:
                df.loc[df["category"] == category, "service_count"] += count
                print(f"[VehicleCategoryRepository] Updated '{category}' count to {df.loc[df['category'] == category, 'service_count'].values[0]}")
            else:
                df = pd.concat(
                    [df, pd.DataFrame([{"category": category, "service_count": count}])],
                    ignore_index=True
                )
                print(f"[VehicleCategoryRepository] Added new category '{category}' with count {count}")

        # Save back to MySQL (overwrite table)
        print(f"[VehicleCategoryRepository] Saving updated DataFrame to MySQL:\n{df}")
        with engine.begin() as conn:
            df.to_sql(self.table_name, con=conn, if_exists="replace", index=False)

        print("[VehicleCategoryRepository] Save complete.\n")
        return df.to_dict(orient="records")
