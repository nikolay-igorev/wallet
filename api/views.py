from decimal import Decimal

from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status, viewsets, permissions, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Wallet, Operation
from api.serializers import WalletSerializer, OperationSerializer

@extend_schema_view(
    retrieve=extend_schema(
            description="Получение баланса кошелька.",
        ),
)
class WalletViewSet(mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [permissions.AllowAny]


class OperationViewSet(mixins.CreateModelMixin,
                       viewsets.GenericViewSet):
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=["post"])
    def operation(self, request, wallet_uuid):
        """Изменение счета кошелька (снятие и пополнение)."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():

            try:
                wallet = get_object_or_404(Wallet, uuid=wallet_uuid)
            except Wallet.DoesNotExist:
                return Response({"detail": "The wallet does not exist."}, status=status.HTTP_404_NOT_FOUND)

            if serializer.validated_data["type"] == "deposit":
                wallet.balance += Decimal(serializer.validated_data["amount"])
                wallet.save()

                Operation.objects.create(
                    wallet=wallet,
                    type=serializer.validated_data["type"],
                    amount=serializer.validated_data["amount"],
                )

                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

            elif serializer.validated_data["type"] == "withdraw":

                if wallet.balance >= Decimal(serializer.validated_data["amount"]):
                    wallet.balance -= Decimal(serializer.validated_data["amount"])
                    wallet.save()

                    Operation.objects.create(
                        wallet=wallet,
                        type=serializer.validated_data["type"],
                        amount=serializer.validated_data["amount"],
                    )

                    headers = self.get_success_headers(serializer.data)
                    return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

                else:
                    return Response({"detail": "Not enough money on the wallet."},
                                    status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
