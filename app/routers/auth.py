from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from jose import jwt
from datetime import datetime, timedelta
import bcrypt
import os
from app.database import database, users_table

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey123")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

class RegisterRequest(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/register", status_code=201)
async def register(request: RegisterRequest):
    existing = await database.fetch_one(
        users_table.select().where(users_table.c.username == request.username)
    )
    if existing:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    hashed = bcrypt.hashpw(request.password.encode(), bcrypt.gensalt()).decode()
    await database.execute(
        users_table.insert().values(username=request.username, hashed_password=hashed)
    )
    return {"message": "Usuario creado exitosamente"}

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    user = await database.fetch_one(
        users_table.select().where(users_table.c.username == request.username)
    )
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    if not bcrypt.checkpw(request.password.encode(), user["hashed_password"].encode()):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    token = create_access_token({"sub": request.username})
    return {"access_token": token, "token_type": "bearer"}