from datetime import datetime
from base.models import UUIDModel
from django.db import models
from django.conf import settings
from django.db.models.manager import BaseManager

# Create your models here.

class Category(UUIDModel):
    owner = models.ForeignKey(
        getattr(settings, 'AUTH_USER_MODEL'),
        related_name='my_wallet_categories',
        on_delete=models.PROTECT
    )
    title = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self) -> str:
        return self.title


class Wallet(UUIDModel):
    owner = models.ForeignKey(
        getattr(settings, 'AUTH_USER_MODEL'),
        related_name='my_wallets',
        on_delete=models.PROTECT
    )
    name = models.CharField(max_length=100)

    @property
    def paid_logs(self) -> BaseManager:
        return self.logs.filter(when__lte=datetime.now())

    @property
    def pendent_logs(self) -> BaseManager:
        return self.logs.exclude(when__lte=datetime.now())


class LogBase(UUIDModel):
    title = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    when = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.title

class LogScheduleBase(LogBase):
    schedule = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

class Log(LogScheduleBase):
    wallet = models.ForeignKey(Wallet, related_name='logs', on_delete=models.PROTECT)
    category = models.ForeignKey(Category, related_name='logs', on_delete=models.PROTECT)


class TransferLog(LogScheduleBase):
    from_wallet = models.ForeignKey(Wallet, related_name='+', on_delete=models.PROTECT)
    from_category = models.ForeignKey(Category, related_name='+', on_delete=models.PROTECT)
    to_wallet = models.ForeignKey(Wallet, related_name='+', on_delete=models.PROTECT)
    to_category = models.ForeignKey(Category, related_name='+', on_delete=models.PROTECT)
    withdraw = models.ForeignKey(
        Log,
        related_name='as_withdraw_of_transfer',
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )
    deposit = models.ForeignKey(
        Log,
        related_name='as_deposit_of_transfer',
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )


class SplitedLog(LogBase):
    wallet = models.ForeignKey(Wallet, related_name='splited_logs', on_delete=models.PROTECT)
    category = models.ForeignKey(Category, related_name='splited_logs', on_delete=models.PROTECT)
    number_of_parts = models.PositiveIntegerField()
    day_of_month = models.PositiveSmallIntegerField()
    split_number = models.PositiveSmallIntegerField()


class SplitedLogPart(UUIDModel):
    splited_log = models.ForeignKey(SplitedLog, related_name='parts', on_delete=models.PROTECT)
    log = models.ForeignKey(Log, related_name='as_splited_log_part', on_delete=models.PROTECT)
