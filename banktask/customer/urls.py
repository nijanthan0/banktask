from django.urls import path
from .views import CustomerCreateView, CustomerProfileView, CustomerProfileDelete

urlpatterns = [
    path('customers/', CustomerCreateView.as_view(), name='create_customer'),
    path('customers/<int:pk>/', CustomerProfileView.as_view(), name='customer_profile'),
    path('customers/<int:pk>/hard-delete/', CustomerProfileDelete.as_view(), name='customer_hard_delete'),

]