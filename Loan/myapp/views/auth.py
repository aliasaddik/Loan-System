import secrets
import jwt
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from Loan.myapp.api.permission import UserIsAuthenticated, IsMerchant, IsAdmin
from django.contrib.auth.hashers import check_password, make_password
from Loan.myapp.api.response import CustomResponse
from rest_framework.parsers import MultiPartParser, FormParser
from Loan.myapp.services.users import get_user_by_id, get_user_by_email
from Loan.myapp.services.customers import get_customer_by_id, get_customer_by_email


from Loan.myapp.serializers.auth import (
 RegisterCustomerSerializer,
 MyTokenObtainPairSerializer,
 VerifyEmailSerializer,
 MyTokenRefreshSerializer
)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from Loan.myapp.models.users import USER_TYPE
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings

class CustomerRegisterApiView(GenericAPIView):
    """Class RegisterAPIView to register a new user into database"""
    serializer_class = RegisterCustomerSerializer
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request: Request) -> Response:
        """Method to Onboard a new customer"""
       
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
           
            password_token = secrets.token_hex(16)  
            user = serializer.save(password = make_password(password_token))

             
            send_mail(
    		    subject="complete loan system onboarding",
    		    message= 'Hi '+ serializer.data['first_name']+' Use this password '+ password_token+' along with the code provided by the merchant to login ',
    		    from_email=settings.EMAIL_HOST_USER,
    		    recipient_list=[serializer.data['email']])
           
            data = serializer.data
            data.update({'usercode': user.usercode}) 
            return CustomResponse.success(
                data = data,

                message="User created successfully",
                 
            )
        return CustomResponse.bad_request(
            error=serializer.errors, message="User creation failed"
        )

class VerifyEmailView(GenericAPIView):
    serializer_class = VerifyEmailSerializer
    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.update_customer(serializer.validated_data)
            return CustomResponse.success(message= 'Verification successfual and new password is set')
        else:
            return CustomResponse.bad_request(error=serializer.errors,message='Can not verify') 


class LoginByTokenApiView(TokenObtainPairView):
    """Class LoginByTokenAPIView to login a user by jwt token"""

    serializer_class = MyTokenObtainPairSerializer

    def post(self, request: Request) -> Response:
        """Method to register a new user"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return CustomResponse.success(
                data=serializer.custom_token(data=serializer.data),
                message="User logged in successfully",
            )
        return CustomResponse.bad_request(
            message="Please make sure that you entered a valid data",
            error=serializer.errors,
        )


        


# class MyTokenRefreshView(TokenRefreshView):
#     """
#     An end point to refresh the user token
#     """

#     serializer_class = MyTokenRefreshSerializer


# class VerifySetPasswordView(GenericAPIView):
#     serializer_class = ChangePasswordSerializer

#     def put(self, request: Request) -> Response:
#         token = request.GET.get('token')
#         serializer = self.get_serializer(data=request.data)
#         try:
#             payload = jwt.decode(token, settings.SECRET_KEY)
#             user =  get_user_by_id(id=payload['user_id'])
            
#             if not user.is_verified:
#                 new_password = make_password(serializer.validated_data.get("new_password"))
#                 checked_password: bool = check_password(
#                 serializer.validated_data.get("new_password"), serializer.validated_data.get("verify_new_password")
#             )
#             if serializer.is_valid():
#                 if checked_password:
#                    user.password = new_password
#                    user.is_active=True
#                    user.save()
#                    return CustomResponse.success({'email': 'Successfully activated'} )
#                 return CustomResponse.unauthorized()
#             return CustomResponse.bad_request(
#                 message="Please make sure that you entered a valid data",
#                 error=serializer.errors,
#         )

#         except jwt.ExpiredSignatureError as identifier:
#             return CustomResponse.bad_request({'error': 'Activation Expired'} )
#         except jwt.exceptions.DecodeError as identifier:
#             return CustomResponse.bad_request({'error': 'Invalid token'})
         