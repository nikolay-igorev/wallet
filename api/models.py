import uuid
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Wallet(models.Model):
    """Модель кошелька"""
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    balance = models.DecimalField(max_digits=11, decimal_places=2, validators=[MinValueValidator(Decimal(0.0))])


class Operation(models.Model):
    """Модель операции над кошельком"""
    OPERATION_TYPE_CHOICES = {
        "deposit": "Deposit",
        "withdraw": "Withdraw",
    }

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    type = models.CharField(max_length=11, choices=OPERATION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=11, decimal_places=2, validators=[MinValueValidator(Decimal(0.0))])
