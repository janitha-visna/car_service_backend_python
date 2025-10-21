from app.dto.service_entry_dto import ServiceEntryData
from app.processors.base_processor import BaseProcessor

class ServiceEntryCoordinator:
    def __init__(self, processors: list[BaseProcessor]):
        self.processors = processors

    def execute(self, entry: ServiceEntryData):
        results = {}
        for processor in self.processors:
            result = processor.process(entry)
            if result:
                results[processor.__class__.__name__] = result
        return {
            "status": "success",
            "analytics": results
        }