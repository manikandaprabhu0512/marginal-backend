from fastapi import APIRouter, Depends, Request, Response, status

from db.crud import db_login_user, db_register_user
from db.dtos import LoginRequest, UserResponse, UserSchema
from db.models import User
from middleware.auth_middleware import verifyToken

router = APIRouter(prefix="/user")

@router.get("/health")
async def get_health():
    return {"status": "ok"}

@router.post("/register", response_model= UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(body: UserSchema):
    user = await db_register_user(body)
    return user

@router.post("/login", response_model = UserResponse, status_code=status.HTTP_200_OK)
async def login_user(body: LoginRequest, response: Response):
    user, tokens = await db_login_user(body)

    response.set_cookie(
        key="accessToken",
        value=tokens["access_token"],
        httponly=True,
        secure=True,
        samesite="none",
        max_age=7 * 24 * 60 * 60,
    )

    response.set_cookie(
        key="refreshToken",
        value=tokens["refresh_token"],
        httponly=True,
        secure=True,
        samesite="none",
        max_age=7 * 24 * 60 * 60,
    )

    return user

@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout_user(response: Response, _: User = Depends(verifyToken)):
    response.delete_cookie("accessToken")
    response.delete_cookie("refreshToken")

    return {"status": "ok"}

@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(current_user: User = Depends(verifyToken)):
    return current_user