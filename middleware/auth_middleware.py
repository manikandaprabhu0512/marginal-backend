import os

import jwt
from fastapi import HTTPException, Request, status

from db.models import User


async def verifyToken(request: Request):
    try:
        access_token = request.cookies.get("accessToken")

        if access_token is None:
            auth_header = request.headers.get("Authorization")

            if auth_header is not None:
                access_token = auth_header.removeprefix("Bearer ").strip()

        if access_token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token Expired"
            )

        secret = os.getenv("ACCESS_TOKEN_SECRET_KEY")
        algorithm = os.getenv("ALGORITHM", "HS256")

        decodedToken = jwt.decode(access_token, secret, algorithms=[algorithm])

        print(decodedToken)
        print(decodedToken["_id"])
        print(decodedToken["username"])

        print("Finding User...")
        user = await User.get(decodedToken["_id"])
        print("User Found...")

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User doesn't exists. Invalid Action."
            )

        print(user)

        return user

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )