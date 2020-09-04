import hashlib

from fastapi import APIRouter

from app.models import User
from .payloads import UserBody as UserPayload

router = APIRouter()


@router.post('/users/', status_code=201)
async def register_user(body: UserPayload):
    password = body.password.encode('utf8')
    hashed = hashlib.md5(password).hexdigest()

    await User.create(email=body.email, password=hashed)

    return {'data': {'status': 'OK', 'email': body.email}}
