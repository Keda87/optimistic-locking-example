from tortoise import fields
from tortoise.models import Model


class Voucher(Model):
    id = fields.BigIntField(pk=True)
    promo_code = fields.CharField(max_length=120)
    quota = fields.IntField()
    total_redeemed = fields.IntField(default=0)
    version = fields.IntField(default=1)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = 'vouchers'

    def __str__(self):
        return self.promo_code


class VoucherLog(Model):
    id = fields.BigIntField(pk=True)
    user = fields.ForeignKeyField('models.User', on_delete=fields.CASCADE)
    voucher = fields.ForeignKeyField('models.Voucher', on_delete=fields.CASCADE)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = 'voucher_logs'
        unique_together = [
            ['user', 'voucher']
        ]
