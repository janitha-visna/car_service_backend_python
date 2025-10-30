# app/repositories/FailedServiceEntryRepository.py
from app.repositories.base_repository import BaseRepository
from app.database.FailedServiceEntryModel import FailedServiceEntry

class FailedServiceEntryRepository(BaseRepository):
    def log_failure(self, entry, error_message: str):
        failed = FailedServiceEntry(
            number_plate=entry.number_plate,
            vehicle_type=entry.vehicle_type,
            amount=entry.amount,
            error_message=error_message,
        )
        self.db.add(failed)
        self.commit()
        self.close()
