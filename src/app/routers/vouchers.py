from fastapi import APIRouter, Depends, HTTPException, status
from tortoise.transactions import atomic

from app.middlewares.basic import get_current_user
from app.misc.exceptions import RedeemException
from app.models import Voucher, User
from app.routers.payloads import VoucherBody as VoucherPayload, RedeemBody
from app.routers.services.vouchers import redeem_voucher_logic

router = APIRouter()


@atomic
@router.post('/vouchers/redeem/')
async def redeem_voucher(body: RedeemBody, user: User = Depends(get_current_user)):
    try:
        await redeem_voucher_logic(body, user)
    except RedeemException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )
    return {'data': {'status': 'OK'}}


@router.post('/vouchers/')
async def create_voucher(body: VoucherPayload):
    await Voucher.create(
        promo_code=body.promo_code,
        quota=body.quota,
    )
    return {'data': body.dict()}
