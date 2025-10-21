from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Example MySQL connection string
DATABASE_URL = "mysql+pymysql://root@localhost:3306/car_service"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()