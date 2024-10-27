from django.db import models
from banktask.customer.models import Customer
from django.utils import timezone

# Create your models here.
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('withdraw', 'Withdraw'),
        ('transfer', 'Transfer'),
        ('deposit', 'Deposit'),
    ]
    FLOW_TYPES = [
        ('credit', 'Credit'),
        ('debit', 'Debit')
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
    flow_type = models.CharField(max_length=10, choices=FLOW_TYPES, null=True)
    rel_customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='related_transactions')

    def __str__(self):
        return f"{self.transaction_type} - {self.flow_type} - {self.amount} - {self.customer.name}"