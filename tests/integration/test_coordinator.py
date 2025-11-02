import pytest
from app.database.connection import SessionLocal, Base, engine
from app.coordinator.service_entry_coordinator import ServiceEntryCoordinator
from app.dto.service_entry_dto import ServiceEntryData
from sqlalchemy import Column, Integer, String

# Temporary model for testing
class DummyModel(Base):
    __tablename__ = "dummy_table"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))

Base.metadata.create_all(bind=engine)


# Fake processors for testing
class ProcessorA:
    def __init__(self, db):
        self.db = db
    def process(self, entry):
        self.db.add(DummyModel(name="ProcessorA"))
        return True


class ProcessorB:
    def __init__(self, db):
        self.db = db
    def process(self, entry):
        raise Exception("Simulated failure in ProcessorB")


class ProcessorC:
    def __init__(self, db):
        self.db = db
    def process(self, entry):
        self.db.add(DummyModel(name="ProcessorC"))
        return True


# Monkey-patch coordinator to use our dummy processors
def test_transaction_rollback():
    coordinator = ServiceEntryCoordinator()
    coordinator.processors = [ProcessorA, ProcessorB, ProcessorC]

    entry = ServiceEntryData(
        number_plate="TEST123",
        vehicle_type="car",
        service_types=["oil_change", "filter_change"],
        amount=2500,
        date="2025-09-30",
        start_time="09:30",
        end_time="10:15",
        telephone_number="0771234567"
    )

    # Run coordinator (expect exception)
    try:
        coordinator.run(entry)
    except Exception:
        pass

    # Check database state
    db = SessionLocal()
    records = db.query(DummyModel).all()
    db.close()

    assert len(records) == 0, "Rollback failed — records still exist!"
