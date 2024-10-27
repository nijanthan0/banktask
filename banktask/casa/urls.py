from django.urls import path
from .views import WithdrawView, TransferView, CustomerTransactionHistoryView, DepositView

urlpatterns = [
    path('casa/withdraw/<int:pk>/', WithdrawView.as_view(), name='customer_withdraw'),
    path('casa/deposit/<int:pk>/', DepositView.as_view(), name='customer_deposit'),
    path('casa/transfer/<int:pk>/', TransferView.as_view(), name='customer_transfer'),
    path('casa/transaction/<int:pk>/', CustomerTransactionHistoryView.as_view(), name='customer_transaction'),

]