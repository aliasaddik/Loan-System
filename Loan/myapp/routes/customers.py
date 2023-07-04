from django.urls import path
from Loan.myapp.views.customers import (
   AdminCustomerAPIView,
   AdminCustomerListAPIView,)

urlpatterns = [
    path("", AdminCustomerListAPIView.as_view(), name="list all customers"),
    path(":<int:id>/", AdminCustomerAPIView.as_view(), name="get a customer"),
]
