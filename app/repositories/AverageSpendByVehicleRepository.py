from app.database.connection import SessionLocal
from app.models.AverageSpendByVehicleModel import AverageSpendByVehicle
from app.config.logger import repository_logger
from app.repositories.base_repository import BaseRepository

class AverageSpendByVehicleRepository(BaseRepository):
    def save_average_spend(self, summary_df):

        repository_logger.info("Saving average spend by vehicle type (month-wise)...")

        try:
            for _, row in summary_df.iterrows():
                existing = self.db.query(AverageSpendByVehicle).filter_by(
                    vehicle_type=row["vehicle_type"],
                    year=int(row["year"]),
                    month=int(row["month"])
                ).first()

                if existing:
                    repository_logger.debug(
                        f"Updating {row['vehicle_type']} for {row['year']}-{row['month']} with new average {row['average_spend']}"
                    )
                    existing.average_spend = float(row["average_spend"])
                else:
                    repository_logger.debug(
                        f"Inserting {row['vehicle_type']} for {row['year']}-{row['month']} average {row['average_spend']}"
                    )
                    self.db.add(
                        AverageSpendByVehicle(
                            vehicle_type=row["vehicle_type"],
                            year=int(row["year"]),
                            month=int(row["month"]),
                            average_spend=float(row["average_spend"])
                        )
                    )


            repository_logger.info("✅ Average spend by vehicle type saved successfully")
        except Exception as e:

            repository_logger.exception(f"Error saving average spend data: {e}")
        finally:

            repository_logger.debug("Database session closed for AverageSpendByVehicleRepository.")
