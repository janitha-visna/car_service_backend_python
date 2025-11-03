from abc import ABC,abstractmethod

from sqlalchemy.orm import Session

from app.dto.service_entry_dto import ServiceEntryData

class BaseProcessor(ABC):
    def __init__(self, db: Session):
        """
        All processors receive a shared DB session from the coordinator.
        """
        self.db = db
    @abstractmethod
    def process(self,entry:ServiceEntryData):
        pass