from sqlalchemy.orm import Session
from passlib.context import CryptContext

from models import (
    User, PersonalInfo, TrainingAvailability, Condition, Password
)
from schemas import UserCreate

_pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --------------------------------------------------------- #
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_cpf(db: Session, cpf: str):
    return db.query(User).filter(User.cpf == cpf).first()

# --------------------------------------------------------- #
def create_user_full(db: Session, data: UserCreate):
    # 1) cria hash e Password
    hashed = _pwd_ctx.hash(data.password)
    pwd_row = Password(password256=hashed)
    db.add(pwd_row)
    db.flush()                  # garante pwd_row.id

    # 2) sub-objetos auxiliares
    cond   = Condition(**data.condition.model_dump())
    pinfo  = PersonalInfo(**data.personal_info.model_dump())
    avail  = TrainingAvailability(**data.training_availability.model_dump())

    # 3) usuário em si
    user = User(
        first_name = data.first_name,
        last_name  = data.last_name,
        cpf        = data.cpf,
        birth_date = data.birth_date,
        email      = data.email,
        phone_number = data.phone_number,
        id_password  = pwd_row.id,
        personal_info         = pinfo,
        training_availability = avail,
        condition             = cond,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# --------------------------------------------------------- #
def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not user.password_obj:
        return None
    if not _pwd_ctx.verify(password, user.password_obj.password256):
        return None
    return user
