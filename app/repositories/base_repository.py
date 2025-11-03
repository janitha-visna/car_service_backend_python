from app.database.connection import SessionLocal


class BaseRepository:
    def __init__(self):
        """
        Always create a new DB session for this repository.
        """
        self.db = SessionLocal()

    def commit(self):
        """Commit the session."""
        self.db.commit()

    def rollback(self):
        """Rollback the session."""
        self.db.rollback()

    def close(self):
        """Close the session."""
        self.db.close()