from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base() # base class for models (blueprint for db models)

def User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, autoincrement=True)
    email = Column(String(100), unique=True, default="N/A")
    name = Column(String(100), unique=True, default="Unknown")