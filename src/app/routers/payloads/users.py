from pydantic.main import BaseModel


class UserBody(BaseModel):
    email: str
    password: str
