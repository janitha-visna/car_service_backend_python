from app.database.connection import SessionLocal
from app.dto.service_entry_dto import ServiceEntryData
from app.processors.base_processor import BaseProcessor
from app.config.logger import logger

class ServiceEntryCoordinator:
    def __init__(self, processors: list[type[BaseProcessor]]):
        """
        :param processors: List of processor classes (not instances)
        """
        self.processor_classes = processors
       # self.failed_repo = FailedServiceEntryRepository()

    def execute(self, entry: ServiceEntryData):
        db = SessionLocal()  # single shared session for all processors
        results = {}

        try:
            # Instantiate processors using a for loop
            processors = []
            for cls in self.processor_classes:
                processor_instance = cls(db)
                processors.append(processor_instance)

            # Execute each processor
            for processor in processors:
                logger.info(f"▶ Running {processor.__class__.__name__}")
                result = processor.process(entry)
                if result:
                    results[processor.__class__.__name__] = result

            # Commit only once after all processors succeed
            db.commit()
            logger.info("✅ All processors executed successfully")

            return {
                "status": "success",
                "analytics": results
            }

        except Exception as e:
            # Rollback if anything fails
            db.rollback()
            logger.exception(f"❌ Transaction failed: {e}")

            # Log failed entry for analysis
            self.failed_repo.log_failure(entry, str(e))

            return {
                "status": "failed",
                "error": str(e),
                "failed_entry": entry.dict(),
            }

        finally:
            db.close()
            logger.debug("Database session closed for ServiceEntryCoordinator.")