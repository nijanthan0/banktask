from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Transaction
from banktask.customer.models import Customer
from .serializers import TransactionSerializer, TransactionTransferSerializer, TransactionWithdrawlSerializer
from drf_yasg.utils import swagger_auto_schema

class WithdrawView(APIView):
    """
    Withdraw funds from a customer's account.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=TransactionWithdrawlSerializer)
    def post(self, request, pk, format=None):
        try:
            customer = Customer.objects.get(pk=pk, is_active=1)
            amount = request.data.get('amount')

            if not amount or float(amount) <= 0:
                return Response({"error": "Invalid amount."}, status=status.HTTP_400_BAD_REQUEST)

            if customer.dep < float(amount):
                return Response({"error": "Insufficient funds."}, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                customer.dep = float(customer.dep) - float(amount)
                customer.save()

                # Create a transaction record
                Transaction.objects.create(
                    customer=customer,
                    transaction_type='withdraw',
                    flow_type='debit',
                    amount=amount
                )

            return Response({"message": "Withdrawal successful."}, status=status.HTTP_200_OK)

        except Customer.DoesNotExist:
            return Response({"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

class TransferView(APIView):
    """
    Transfer funds from one customer account to another.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=TransactionTransferSerializer)
    def post(self, request, pk, format=None):
        try:
            sender = Customer.objects.get(pk=pk, is_active=1)
            receiver_id = request.data.get('rel_customer')
            amount = request.data.get('amount')

            if not receiver_id or not amount or float(amount) <= 0:
                print(receiver_id, amount)
                return Response({"error": "Invalid receiver or amount."}, status=status.HTTP_400_BAD_REQUEST)

            if sender.dep < float(amount):
                return Response({"error": "Insufficient funds."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                receiver = Customer.objects.get(pk=receiver_id, is_active=1)
            except Customer.DoesNotExist:
                return Response({"error": "Receiver not found."}, status=status.HTTP_404_NOT_FOUND)

            with transaction.atomic():
                # Deduct from sender
                sender.dep = float(sender.dep) - float(amount)
                sender.save()

                # Add to receiver
                receiver.dep = float(receiver.dep) + float(amount)
                receiver.save()

                # Create transaction records for both sender and receiver
                Transaction.objects.create(
                    customer=sender,
                    transaction_type='transfer',
                    amount=amount,
                    flow_type='debit',
                    rel_customer=receiver
                )
                Transaction.objects.create(
                    customer=receiver,
                    transaction_type='transfer',
                    amount=amount,
                    flow_type='credit',
                    rel_customer=sender
                )

            return Response({"message": "Transfer successful."}, status=status.HTTP_200_OK)

        except Customer.DoesNotExist:
            return Response({"error": "Sender not found."}, status=status.HTTP_404_NOT_FOUND)

class DepositView(APIView):
    """
    Deposits funds in a customer's account.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=TransactionWithdrawlSerializer)
    def post(self, request, pk, format=None):
        try:
            customer = Customer.objects.get(pk=pk, is_active=1)
            amount = request.data.get('amount')

            with transaction.atomic():
                customer.dep = float(customer.dep) + float(amount)
                customer.save()

                # Create a transaction record
                Transaction.objects.create(
                    customer=customer,
                    transaction_type='deposit',
                    flow_type='credit',
                    amount=amount
                )

            return Response({"message": "Deposited successful."}, status=status.HTTP_200_OK)

        except Customer.DoesNotExist:
            return Response({"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

class CustomerTransactionHistoryView(APIView):
    """
    View the transaction history of a customer's account.
    """
    authentication_classes = [JWTAuthentication]  # Specify JWT authentication
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        try:
            customer = Customer.objects.get(pk=pk, is_active=1)
            transactions = customer.transactions.all()
            serializer = TransactionSerializer(transactions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Customer.DoesNotExist:
            return Response({"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)
