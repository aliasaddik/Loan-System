from django.urls import path
from Loan.myapp.views.installments import (
    CustomerInstallmentAPIView,
    InstallmentsAPIView,)
urlpatterns = [
    path("my_installments/", CustomerInstallmentAPIView.as_view(), name="get installments of a customer"),
    path("accept_loan/<int:id>/", InstallmentsAPIView.as_view(), name="accept loan"),
    
]

