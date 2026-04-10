from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import Token
from app.services.user import UserService
from app.services.token import TokenService

router = APIRouter(prefix="/auth", tags=["auth"])

user_service = UserService()
token_service = TokenService()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(body: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await user_service.get_user_by_username(db, body.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")

    user = await user_service.create_user(db, body.username, body.password)
    return user


@router.post("/login", response_model=Token)
async def login(body: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await user_service.get_user_by_username(db, body.username)
    if not user or not user_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = token_service.create_access_token(user.id)
    return {"access_token": token, "token_type": "bearer"}
