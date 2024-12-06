from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_URL = "postgresql://postgres:123456@db:5432/postgres"
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
