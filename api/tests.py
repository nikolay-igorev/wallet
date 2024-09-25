import random
from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from api.models import Wallet

client = APIClient()


class WalletTest(APITestCase):
    def setUp(self) -> None:
        for _ in range(1, 10):
            baker.make(Wallet)

        self.wallet = Wallet.objects.order_by('?').first()

    def test_get_wallet(self):
        url = reverse('wallet-detail', args=(self.wallet.uuid,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(url, f'/api/v1/wallets/{self.wallet.uuid}/')
        self.assertEqual(response.data['uuid'], str(self.wallet.uuid))


class OperationTest(APITestCase):
    def setUp(self) -> None:
        for _ in range(1, 10):
            baker.make(Wallet)

        self.wallet = Wallet.objects.order_by('?').first()
        self.amount = self.wallet.balance - random.randint(1, 100) if self.wallet.balance - random.randint(1,100) > 0 else 0.0
        self.amount_wrong = self.wallet.balance + random.randint(1, 100)
        self.uuid_wrong = '6f9a9a65-bbee-4217-9f4f-06fce8158465'

    def test_operation_deposit(self):
        start_balance = self.wallet.balance
        url = reverse('operation', args=(self.wallet.uuid,))
        data = {
            "type": "deposit",
            "amount": self.amount
        }
        response = self.client.post(url, data, format='json')
        self.wallet.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(start_balance + self.amount, self.wallet.balance)

    def test_operation_withdraw(self):
        start_balance = self.wallet.balance
        url = reverse('operation', args=(self.wallet.uuid,))
        data = {
            "type": "withdraw",
            "amount": self.amount
        }
        response = self.client.post(url, data, format='json')
        self.wallet.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(start_balance - self.amount, self.wallet.balance)

    def test_operation_withdraw_wrong(self):
        url = reverse('operation', args=(self.wallet.uuid,))
        data = {
            "type": "withdraw",
            "amount": self.amount_wrong
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_operation_wrong_uuid(self):
        url = reverse('operation', args=(self.uuid_wrong,))
        data = {
            "type": "deposit",
            "amount": self.amount
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_operation_wrong_operation(self):
        url = reverse('operation', args=(self.wallet.uuid,))
        data = {
            "type": "bgjdlagbj",
            "amount": self.amount
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_operation_wrong_amount(self):
        url = reverse('operation', args=(self.wallet.uuid,))
        data = {
            "type": "deposit",
            "amount": 'gfdgfdsa'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
