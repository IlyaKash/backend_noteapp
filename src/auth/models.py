from sqlalchemy import Column, Integer, String
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from database import Base

#Base=declarative_base()

class User(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True, index=True)
    username=Column(String, unique=True, index=True)
    email=Column(String, unique=True, index=True)
    hashed_password=Column(String)
    telegram_id=Column(String, unique=True, nullable=True)
    notes=relationship("Note", back_populates="users")