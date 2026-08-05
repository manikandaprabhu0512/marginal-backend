from fastapi import HTTPException, status

from db.models import User


async def generateAccessandRefreshTokens(user: User) -> dict[str, str]:
    try:
        access_token = user.generate_access_token()
        refresh_token = user.generate_refresh_token()

        return {
            "access_token": access_token, 
            "refresh_token": refresh_token
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )