# routers/auth.py
import json
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import secrets
from typing import Annotated
import requests
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
load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET")          # substitua por valor fixo no .env
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
    # # Salva o payload em um arquivo JSON para debug
    # with open("payload_debug.json", "w") as f:
    #     f.write(json.dumps(payload.dict(), indent=4, default=str))

    # Verifica se o CPF e o e-mail já estão cadastrados, evitando duplicidade
    if get_user_by_email(db, payload.email):
        raise HTTPException(400, detail="E-mail já cadastrado")
    if get_user_by_cpf(db, payload.cpf):
        raise HTTPException(400, detail="CPF já cadastrado")

    # chama crud centralizado
    user = create_user_full(db, payload)
    
    # Função que faz requisição pro microserviço de AI que cria o plano de treino
    URL_API_AI = os.getenv("URL_API_AI")
    if not URL_API_AI:
        raise RuntimeError("Defina a env var URL_API_AI")
    response = requests.post(URL_API_AI, json={"user_id": user.id, "available_time": payload.available_time})

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
    token  = jwt.encode({"id": user.id,"sub": user.email, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
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
