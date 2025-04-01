from fastapi import status
from fastapi import Depends
from fastapi import Response
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.user import User

from src.db.session import get_session

from src.repositories.auth import hash_password
from src.repositories.user import UserRepository
from src.repositories.auth import verify_password
from src.repositories.auth import create_access_token
from src.repositories.auth import create_refresh_token
from src.repositories.dependence import get_current_user

from src.schemas.auth import SUserAuth
from src.schemas.auth import SUserPassword


router = APIRouter()


@router.post("/login", tags=["Auth"], summary="Login user")
async def login_user(
        response: Response,
        user_auth: SUserAuth,
        db: AsyncSession = Depends(get_session)
):
    try:
        user_repo = UserRepository(db=db)

        user = await user_repo.get(email=user_auth.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        if not verify_password(user_auth.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password"
            )

        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})

        user.password = None

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "data": user
        }

    except HTTPException as http_err:
        raise http_err


@router.get("/me", tags=["Auth"], summary="Get current user")
async def get_current_user_router(
        current_user: User = Depends(get_current_user)
):
    return current_user


@router.post("/refresh-token", tags=["Auth"], summary="Refresh token")
async def refresh_token(
        response: Response,
        db: AsyncSession = Depends(get_session),
        token: str = None
):
    try:
        if not token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token is required"
            )

        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=token
        )

        user = await get_current_user(credentials=credentials, session=db)

        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    except HTTPException as http_err:
        raise http_err


@router.post("/forget-password", tags=["Auth"], summary="Reset password")
async def forget_password(
    user_auth: SUserAuth,
    db: AsyncSession = Depends(get_session)
):
    user_repo = UserRepository(db=db)
    user = await user_repo.get(email=user_auth.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    copy_user = user.copy()
    if user_auth.password:
        hashed_password = hash_password(user_auth.password)
        copy_user.password = hashed_password

    await user_repo.update(user, copy_user)

    return {"status": "Password updated successfully"}


@router.post("/reset-password", tags=["Auth"], summary="Reset password")
async def reset_password(
    user_auth: SUserPassword,
    db: AsyncSession = Depends(get_session)
):
    user_repo = UserRepository(db=db)

    user = await user_repo.get(email=user_auth.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not verify_password(user_auth.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Password is incorrect"
        )

    hashed_password = hash_password(user_auth.new_password)
    user.password = hashed_password

    await user_repo.update(user, user)

    return {"status": "Password updated successfully"}
