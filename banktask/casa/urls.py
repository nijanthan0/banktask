from django.urls import path
from .views import WithdrawView, TransferView, CustomerTransactionHistoryView

urlpatterns = [
    path('casa/withdraw/<int:pk>/', WithdrawView.as_view(), name='customer_withdraw'),
    path('casa/transfer/<int:pk>/', TransferView.as_view(), name='customer_transfer'),
    path('casa/transaction/<int:pk>/', CustomerTransactionHistoryView.as_view(), name='customer_transaction'),

]