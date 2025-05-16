from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, EmailStr


# ---------- auxiliares ----------
class ConditionIn(BaseModel):
    diabetes: bool = False
    hyper_tension: bool = False
    cardiovascular_disease: bool = False
    obesity: bool = False
    asthma: bool = False
    arthritis: bool = False
    osteoporosis: bool = False
    chronic_back_pain: bool = False
    damaged_left_upper_body: bool = False
    damaged_right_upper_body: bool = False
    damaged_left_lower_body: bool = False
    damaged_right_lower_body: bool = False
    damaged_body_core: bool = False
    recent_surgery: bool = False
    pregnancy: bool = False

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
    username: str
    cpf: str
    birth_date: datetime
    email: EmailStr
    phone_number: str
    password: str                             # texto puro: será hasheado
    personal_info: PersonalInfoIn
    training_availability: TrainingAvailabilityIn
    condition: ConditionIn
    available_time: Optional[str] = None

class UserRead(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    cpf: str
    birth_date: datetime
    email: EmailStr
    phone_number: str

    model_config = {"from_attributes": True}
