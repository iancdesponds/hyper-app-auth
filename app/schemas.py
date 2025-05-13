from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, EmailStr


# ---------- auxiliares ----------
class ConditionIn(BaseModel):
    diabetes: Optional[bool] = None
    hyper_tension: Optional[bool] = None
    cardiovascular_disease: Optional[bool] = None
    obesity: Optional[bool] = None
    asthma: Optional[bool] = None
    arthritis: Optional[bool] = None
    osteoporosis: Optional[bool] = None
    chronic_back_pain: Optional[bool] = None
    damaged_left_upper_body: Optional[bool] = None
    damaged_right_upper_body: Optional[bool] = None
    damaged_left_lower_body: Optional[bool] = None
    damaged_right_lower_body: Optional[bool] = None
    damaged_body_core: Optional[bool] = None
    recent_surgery: Optional[bool] = None
    pregnancy: Optional[bool] = None

    model_config = {"from_attributes": True}

class PersonalInfoIn(BaseModel):
    weight_kg: int
    height_cm: int
    bio_gender: Literal["M", "F", "O"]
    training_since: datetime

    model_config = {"from_attributes": True}

class TrainingAvailabilityIn(BaseModel):
    sunday: bool
    monday: bool
    tuesday: bool
    wednesday: bool
    thursday: bool
    friday: bool
    saturday: bool

    model_config = {"from_attributes": True}

# ---------- usuário ----------
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    cpf: str
    birth_date: datetime
    email: EmailStr
    phone_number: str
    password: str                             # texto puro: será hasheado
    personal_info: PersonalInfoIn
    training_availability: TrainingAvailabilityIn
    condition: ConditionIn

class UserRead(BaseModel):
    id: int
    first_name: str
    last_name: str
    cpf: str
    birth_date: datetime
    email: EmailStr
    phone_number: str

    model_config = {"from_attributes": True}
