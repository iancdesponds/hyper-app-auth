from sqlalchemy.orm import Session
from passlib.context import CryptContext

from models import User, UserCreate, Password


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_cpf(db: Session, cpf: str):
    return db.query(User).filter(User.cpf == cpf).first()

def create_user(db: Session, data: UserCreate):
    # 1) Hash da senha e criação do registro em password
    hashed = pwd_context.hash(data.password)
    pwd = Password(password256=hashed)
    db.add(pwd)
    db.flush()  # atribui pwd.id sem commitar

    # 2) Criação do usuário referenciando password.id
    user = User(
        first_name=data.first_name,
        last_name=data.last_name,
        cpf=data.cpf,
        birth_date=data.birth_date,
        email=data.email,
        phone_number=data.phone_number,
        id_password=pwd.id
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not user.password_obj:
        return None
    if not pwd_context.verify(password, user.password_obj.password256):
        return None
    return user
