# app/Http/Controllers/AuthController.py

from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from sqlalchemy.orm import sessionmaker

from app.Http.Controllers.Controller import Controller
from app.Models.User import User
from vendor.Illuminate.Console import database
from .auth_helpers import create_access_token # Kita akan buat file ini

# --- Konfigurasi ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
engine = database.get_engine()
SessionLocal = sessionmaker(bind=engine)

# --- Pydantic Schemas (untuk validasi & Swagger) ---
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# --- Controller ---
class AuthController(Controller):

    async def register(self, user_data: UserCreate):
        session = SessionLocal()
        # Cek jika email atau username sudah ada
        db_user = session.query(User).filter((User.email == user_data.email) | (User.username == user_data.username)).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Email or username already registered")

        # Buat user baru
        hashed_password = pwd_context.hash(user_data.password[:72])
        new_user = User(email=user_data.email, username=user_data.username, password_hash=hashed_password)

        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        session.close()

        # Buat token
        access_token = create_access_token(data={"sub": new_user.email})
        return {"access_token": access_token, "token_type": "bearer"}

    async def login(self, form_data: UserLogin):
        session = SessionLocal()
        user = session.query(User).filter(User.email == form_data.email).first()
        session.close()

        if not user or not pwd_context.verify(form_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}
