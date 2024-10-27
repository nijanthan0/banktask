from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Transaction
from banktask.customer.models import Customer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User


class TransferTests(APITestCase):

    def setUp(self):
        # Create a customer for testing
        self.customer = Customer.objects.create(name='customer_test1', dep=1000.90)
        self.customer = Customer.objects.create(name='customer_test2', dep=1000)
        self.user = User.objects.create(username='admin', password='pass')
        self.token = RefreshToken.for_user(self.user)

    def test_withdraw_funds(self):
        """
        test withdrawn from the customer's account.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token.access_token))
        url = reverse('customer_withdraw', args=[self.customer.id])
        data = {'customer': self.customer.id, "transaction_type": "withdraw", 'amount': 300}
        response = self.client.post(url, data)
        self.customer.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(self.customer.dep), 700.00)

    def test_deposit_funds(self):
        """
        test deposit in the customer's account.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token.access_token))
        url = reverse('customer_deposit', args=[self.customer.id])
        data = {'customer': self.customer.id, "transaction_type": "deposit", 'amount': 300}
        response = self.client.post(url, data)
        self.customer.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(self.customer.dep), 1300.00)

    def test_transfer_funds(self):
        """
        test amount transferred between two customers.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token.access_token))
        recipient = Customer.objects.create(name='Recipient', dep=500)
        url = reverse('customer_transfer', args=[self.customer.id])
        data = {
            'customer': self.customer.id,
            'rel_customer': recipient.id,
            'transaction_type': "transfer",
            'amount': 400
        }
        response = self.client.post(url, data, format='json')
        self.customer.refresh_from_db()
        recipient.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(self.customer.dep), 600.00)
        self.assertEqual(float(recipient.dep), 900.00)