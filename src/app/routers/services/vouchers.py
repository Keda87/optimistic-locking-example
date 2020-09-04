from tortoise.exceptions import DoesNotExist, IntegrityError

from app.misc.exceptions import RedeemException
from app.models import Voucher, VoucherLog, User
from app.routers.payloads import RedeemBody


async def redeem_voucher_logic(body: RedeemBody, user: User):
    voucher = await Voucher.get(promo_code=body.promo_code)
    try:
        if voucher.total_redeemed < voucher.quota:
            voucher.total_redeemed += 1
            await voucher.save()
            await VoucherLog.create(user=user, voucher=voucher)
        else:
            raise RedeemException('promo code is fully redeemed')
    except DoesNotExist:
        raise RedeemException('invalid promo code')
    except IntegrityError:
        raise RedeemException(f'your account is already redeemed {voucher.promo_code}')

    return Voucher.get(pk=voucher.pk)
