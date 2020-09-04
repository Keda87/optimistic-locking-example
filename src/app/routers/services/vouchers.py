from tortoise.exceptions import DoesNotExist, IntegrityError

from app.misc.exceptions import RedeemException
from app.models import Voucher, VoucherLog, User
from app.routers.payloads import RedeemBody


async def redeem_voucher_logic(body: RedeemBody, user: User):
    try:
        voucher = await Voucher.get(promo_code=body.promo_code)
        if voucher.total_redeemed < voucher.quota:
            is_succeed = await Voucher.filter(
                pk=voucher.pk,
                version=voucher.version
            ).update(
                total_redeemed=voucher.total_redeemed + 1,
                version=voucher.version + 1
            )

            if is_succeed:
                await VoucherLog.create(user=user, voucher=voucher)
            else:
                raise RedeemException('failed to redeem promo code, please try again')
        else:
            raise RedeemException('promo code is fully redeemed')
    except DoesNotExist:
        raise RedeemException('invalid promo code')
    except IntegrityError:
        raise RedeemException(f'your account is already redeemed {body.promo_code}')

    return Voucher.get(pk=voucher.pk)
