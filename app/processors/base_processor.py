from abc import ABC,abstractmethod
from app.dto.service_entry_dto import ServiceEntryData

class BaseProcessor(ABC):
    @abstractmethod
    def process(self,entry:ServiceEntryData):
        pass