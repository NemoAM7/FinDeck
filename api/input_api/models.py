from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

class CSVData(Base):
    __tablename__ = 'csv_data'

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    content = Column(Text)  # Store CSV content directly in the database
    source_type = Column(String)  # 'direct_upload' or 'image_conversion'

# Ensure the database file is created in the api directory
database_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "database.db")
DATABASE_URL = f"sqlite:///{database_path}"  # SQLite database file

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database tables
def init_db():
    # Drop existing tables and recreate them
    Base.metadata.create_all(bind=engine)  # This creates new tables 