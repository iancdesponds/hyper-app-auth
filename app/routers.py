# routers/auth.py
from datetime import datetime, timedelta
import secrets
from typing import Annotated
from passlib.context import CryptContext
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from crud import *

from database import get_db                           # → função que devolve Session
from models import User, PersonalInfo, TrainingAvailability, Condition
from schemas import UserCreate, UserRead
from crud import get_user_by_email, get_user_by_cpf, authenticate_user      # sua função de hashing

# --------------------------------------------------------------------------- #
SECRET_KEY = secrets.token_urlsafe(32)          # substitua por valor fixo no .env
ALGORITHM  = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# --------------------------------------------------------------------------- #

router = APIRouter(prefix="/auth", tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# --------------------------------------------------------------------------- #
# REGISTRO COMPLETO
# --------------------------------------------------------------------------- #
@router.post("/register", response_model=UserRead, status_code=201)
def register_full(payload: UserCreate, db: Session = Depends(get_db)):
    # duplicidade
    if get_user_by_email(db, payload.email):
        raise HTTPException(400, detail="E-mail já cadastrado")
    if get_user_by_cpf(db, payload.cpf):
        raise HTTPException(400, detail="CPF já cadastrado")

    # chama crud centralizado
    user = create_user_full(db, payload)
    return user

# --------------------------------------------------------------------------- #
# LOGIN
# --------------------------------------------------------------------------- #
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db:        Session                   = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token  = jwt.encode({"sub": user.email, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

# --------------------------------------------------------------------------- #
# DEPENDENCY – USER LOGADO
# --------------------------------------------------------------------------- #
def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db:    Session = Depends(get_db)
):
    cred_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str | None = payload.get("sub")
        if email is None:
            raise cred_exc
    except JWTError:
        raise cred_exc

    user = get_user_by_email(db, email)
    if user is None:
        raise cred_exc
    return user

# --------------------------------------------------------------------------- #
# ROTA /me
# --------------------------------------------------------------------------- #
@router.get("/me", response_model=UserRead)
def read_current_user(current_user = Depends(get_current_user)):
    return current_user
