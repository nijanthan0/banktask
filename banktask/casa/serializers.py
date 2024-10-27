from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class TransactionTransferSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ('customer', 'transaction_type', 'amount', 'rel_customer')

class TransactionWithdrawlSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ('customer', 'transaction_type', 'amount')