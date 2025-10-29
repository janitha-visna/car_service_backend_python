from app.dto.service_entry_dto import ServiceEntryData
from app.processors.base_processor import BaseProcessor
from app.config.logger import logger

class ServiceEntryCoordinator:
    def __init__(self, processors: list[BaseProcessor]):
        self.processors = processors

    def execute(self, entry: ServiceEntryData):
        results = {}
        for processor in self.processors:
            try:
                result = processor.process(entry)
                if result:
                    results[processor.__class__.__name__] = result
            except Exception as e:
                logger.exception(f"Processor {processor.__class__.__name__} failed: {e}")
                results[processor.__class__.__name__] = {"error": str(e)}
            # ✅ Console log the results
        print("\n[ServiceEntryCoordinator] Final results:")
        print(results)

        # ✅ Also log to file (optional but good practice)
        logger.info(f"Final analytics results: {results}")

        return {"status": "partial_success", "analytics": results}


