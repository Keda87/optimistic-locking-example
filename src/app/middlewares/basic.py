import hashlib
import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from tortoise.exceptions import DoesNotExist

from app.models import User

security = HTTPBasic()


async def get_current_user(credentials: HTTPBasicCredentials = Depends(security)) -> User:
    try:
        user = await User.get(email=credentials.username)

        hashed = hashlib.md5(credentials.password.encode('utf8')).hexdigest()
        is_password_valid = secrets.compare_digest(user.password, hashed)

        if not is_password_valid:
            raise HTTPException
    except (DoesNotExist, HTTPException):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='incorrect email or password',
            headers={'WWW-Authenticate': 'Basic'}
        )

    return user
