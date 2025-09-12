# models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email=Column(String(200));
    

class Assignment(Base):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    course_name = Column(String(200))
    title = Column(String(200))
    description = Column(Text)
    due_date = Column(DateTime)
