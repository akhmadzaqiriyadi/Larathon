# routes/api.py
from fastapi import APIRouter
from app.Http.Controllers.AuthController import AuthController, UserCreate, UserLogin, Token

# Buat instance controller dan router
auth_controller = AuthController()
router = APIRouter()

# Daftarkan rute register dan login
# Pydantic model di sini akan otomatis membuat dokumentasi Swagger
router.post("/register", response_model=Token, tags=["Authentication"])(auth_controller.register)
router.post("/login", response_model=Token, tags=["Authentication"])(auth_controller.login)
