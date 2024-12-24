from sqlalchemy import Column, Integer, String, ForeignKey
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from database import Base

#Base=declarative_base()

class Note(Base):
    __tablename__="notes"
    id=Column(Integer, primary_key=True, index=True)
    title=Column(String)
    text=Column(String)

    user_id=Column(Integer, ForeignKey("users.id"), nullable=False)

    users=relationship("User", back_populates="notes")