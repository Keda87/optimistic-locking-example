from pydantic.main import BaseModel


class VoucherBody(BaseModel):
    promo_code: str
    quota: int


class RedeemBody(BaseModel):
    promo_code: str
