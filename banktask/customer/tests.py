from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Customer
from django.contrib.auth.models import User

from rest_framework_simplejwt.tokens import RefreshToken

class CustomerTests(APITestCase):

    def setUp(self):
        # Create a customer for testing
        self.customer = Customer.objects.create(name='customer_test1', dep=100.90)
        self.customer = Customer.objects.create(name='customer_test2', dep=100)
        self.user = User.objects.create(username='admin', password='pass')
        self.token = RefreshToken.for_user(self.user)

    def test_create_customer(self):
        """
        Ensure we can create a new customer.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token.access_token))
        url = reverse('create_customer')
        data = {'name': 'New User', 'dep': 500}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 3)
        self.assertEqual(Customer.objects.get(name='New User').dep, 500)



    def test_view_account_balance(self):
        """
        Ensure we can view the customer's account balance.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token.access_token))
        url = reverse('customer_profile', args=[self.customer.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['dep']), 100.00)

