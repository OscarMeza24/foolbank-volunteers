from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    last_name = Column(String, index=True)
    age = Column(Integer)

    # Relaciones
    posts = relationship("Post", back_populates="author")
