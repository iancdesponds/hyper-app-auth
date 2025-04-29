from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    birth = Column(DateTime, unique =False, nullable=True)
    is_active = Column(Boolean, default=True)

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    birth: Optional[datetime.datetime]

    model_config = {
        "from_attributes": True
    }

