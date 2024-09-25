from rest_framework import serializers
from api.models import Wallet, Operation


class WalletSerializer(serializers.ModelSerializer):
    """Сериализация кошелька"""
    class Meta:
        model = Wallet
        fields = ["uuid", "balance"]


class OperationSerializer(serializers.ModelSerializer):
    """Сериализация операции над кошельком"""
    wallet = WalletSerializer(read_only=True)

    class Meta:
        model = Operation
        fields = ["id", "wallet", "type", "amount"]
