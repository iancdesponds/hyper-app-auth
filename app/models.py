# models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()

class PersonalInfo(Base):
    __tablename__ = 'personal_info'
    id = Column(Integer, primary_key=True, autoincrement=True)

class TrainingAvailability(Base):
    __tablename__ = 'training_availability'
    id = Column(Integer, primary_key=True, autoincrement=True)

class Condition(Base):
    __tablename__ = 'condition'
    id = Column(Integer, primary_key=True, autoincrement=True)

class Password(Base):
    __tablename__ = 'password'
    id = Column(Integer, primary_key=True, autoincrement=True)
    password256 = Column(String(256), nullable=False)

    user = relationship('User', back_populates='password_obj', uselist=False)

class User(Base):
    __tablename__ = 'user'

    id             = Column(Integer, primary_key=True, autoincrement=True)
    first_name     = Column(String(45), nullable=False)
    last_name      = Column(String(45), nullable=False)
    cpf            = Column(String(45), unique=True, nullable=False)
    birth_date     = Column(DateTime, nullable=False)
    email          = Column(String(45), unique=True, nullable=False)
    phone_number   = Column(String(15), nullable=False)
    id_infos       = Column(Integer, ForeignKey('personal_info.id'), unique=True)
    id_dates       = Column(Integer, ForeignKey('training_availability.id'), unique=True)
    id_conditions  = Column(Integer, ForeignKey('condition.id'), unique=True)
    id_password    = Column(Integer, ForeignKey('password.id'), unique=True, nullable=True)

    password_obj = relationship('Password', back_populates='user')

# ---------------- Pydantic ----------------
from pydantic import BaseModel, EmailStr, constr
from datetime import datetime as dt

class UserCreate(BaseModel):
    first_name   : constr(strip_whitespace=True, min_length=1, max_length=45)
    last_name    : constr(strip_whitespace=True, min_length=1, max_length=45)
    cpf          : constr(strip_whitespace=True, min_length=11, max_length=14)
    birth_date   : dt
    email        : EmailStr
    phone_number : constr(strip_whitespace=True, min_length=8, max_length=15)
    password     : constr(min_length=6)

class UserRead(BaseModel):
    id           : int
    first_name   : str
    last_name    : str
    cpf          : str
    birth_date   : dt
    email        : EmailStr
    phone_number : str

    model_config = {"from_attributes": True}
