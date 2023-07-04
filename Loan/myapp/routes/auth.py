from django.urls import path
from Loan.myapp.views.auth import (
  CustomerRegisterApiView,
  LoginByTokenApiView,
  VerifyEmailView,

)
urlpatterns = [
    path("onboard/", CustomerRegisterApiView.as_view(), name="onboard a customer"),
    path("login/", LoginByTokenApiView.as_view(), name="login a customer"),
    path("verify/", VerifyEmailView.as_view(), name="verify a customer"),
]