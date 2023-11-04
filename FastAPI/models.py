from sqlalchemy import String, Column,Integer,ForeignKey
from config.db import Base
from sqlalchemy.orm import relationship

class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(225), index=True)
    classes = relationship("Class", back_populates="teacher")

class Class(Base):
    __tablename__='classes'
    id= Column(Integer,primary_key=True, index=True)
    name = Column(String(225), index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    teacher = relationship("Teacher", back_populates="classes")

    