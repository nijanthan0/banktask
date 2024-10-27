from django.shortcuts import render

# Create your views here.
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Customer
from .serializers import CustomerSerializer, CustomerUpdateSerializer
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated


class CustomerCreateView(APIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=CustomerUpdateSerializer)
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        print(serializer)
        last_id = Customer.objects.all().last()
        if not last_id:
            last_id = 0
        else:
            last_id = last_id.id

        # print(last_id.pk)
        if serializer.is_valid():
            # if request.data.get('unique_id', 0) is None:
            serializer.save(unique_id=f"{request.data.get('name', 0)}_{last_id+1}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        serializer = CustomerSerializer(Customer.objects.filter(is_active=1), many=True)
        if serializer:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerProfileView(APIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    # permission_classes = [IsAuthenticated]

    # @swagger_auto_schema()
    def get(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)  # Ensure customer is not soft-deleted
            serializer = CustomerSerializer(customer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
            customer.is_active = 0
            customer.save()  # Save the updated object
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Customer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=CustomerUpdateSerializer)
    def put(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
            serializer = self.serializer_class(customer, data=request.data)

            if serializer.is_valid():
                serializer.save()
            # customer.is_active = 0
            # customer.save()  # Save the updated object
            return Response('Updated object', status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CustomerProfileDelete(generics.DestroyAPIView):
    """
    Hard Delete a customer profile.
    Permanently removes the customer from the database.
    """
    queryset = Customer.objects.all()
    permission_classes = [IsAuthenticated]  # Optional

    def delete(self, request, *args, **kwargs):
        customer = self.get_object()
        customer.delete()  # This performs a hard delete
        return Response('Profile Removed from System', status=status.HTTP_204_NO_CONTENT)