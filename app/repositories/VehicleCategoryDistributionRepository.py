from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.database.VehicleCategoryDistributionModel import VehicleCategoryDistribution
from app.config.logger import logger  # ✅ Import the shared logger


class VehicleCategoryRepository:
    def __init__(self):
        pass

    def update_vehicle_distribution(self, category: str, count: int = 1):
        """
        Updates or inserts the vehicle category distribution record.

        :param category: The vehicle category (e.g., 'Car', 'Bike', etc.)
        :param count: Number to increment (default=1)
        :return: dict containing the updated category and count
        """
        db: Session = SessionLocal()
        logger.info(f"🔄 Updating vehicle category distribution for '{category}' (+{count})")

        try:
            # Check if the category already exists
            existing = db.query(VehicleCategoryDistribution).filter_by(category=category).first()
            if existing:
                existing.service_count += count
                logger.debug(f"Updated '{category}' count to {existing.service_count}")
            else:
                new_entry = VehicleCategoryDistribution(
                    category=category,
                    service_count=count
                )
                db.add(new_entry)
                logger.debug(f"Inserted new category '{category}' with count {count}")

            db.commit()

            updated = db.query(VehicleCategoryDistribution).filter_by(category=category).first()
            logger.info(f"✅ Vehicle category '{category}' updated successfully")

            return {
                "category": updated.category,
                "service_count": updated.service_count
            }

        except Exception as e:
            db.rollback()
            logger.exception(f"❌ Error updating vehicle category '{category}': {e}")
            raise e

        finally:
            db.close()
            logger.debug("Database session closed for VehicleCategoryRepository.")
