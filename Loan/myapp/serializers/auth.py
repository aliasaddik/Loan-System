import hashlib
from django.contrib.auth import get_user_model
from typing import Dict, Any
from rest_framework_simplejwt.serializers import (
     
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework.serializers import(
     ModelSerializer,Serializer,
     CharField,ValidationError,
    EmailField,CharField,DateField,
    IntegerField,BooleanField
  )
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.state import token_backend
from rest_framework import   exceptions
from django.contrib.auth.hashers import check_password,make_password
from Loan.myapp.models.customers import Customer
from Loan.myapp.models.users import USER_TYPE, MyUser
from Loan.myapp.serializers.Image_upload import Base64ImageField
from Loan.myapp.services.users import get_user_by_id, get_user_by_email
from Loan.myapp.services.customers import get_customer_by_usercode

from django.core.validators import EmailValidator, RegexValidator
from django.utils.translation import gettext_lazy as _
from Loan.myapp.validators.integers import is_positive, is_negative1_or_positive

class RegisterCustomerSerializer(ModelSerializer):
    'Register Customer Serializer that can be used by the merchant to onboard a new customer'
    id_front = Base64ImageField(max_length=None, use_url=True)
    id_back = Base64ImageField(max_length=None, use_url=True)

    email = EmailField(
        validators=[EmailValidator()],
        help_text=_('Valid email address required.')
    )
    mobile_number = CharField(
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message=_('Enter a valid mobile number.')
            )
        ],
        help_text=_('Valid mobile number required.')
    )
    date_of_birth = DateField(
        help_text=_('Valid date of birth required.'),
        input_formats=['%Y-%m-%d']
    )
    current_debt_outside = IntegerField(validators= [is_positive])
    credit_history_length = IntegerField(validators= [is_positive])
    pursuit_of_new_credit = IntegerField(validators= [is_positive])
    months_since_last_late_payment = IntegerField(validators= [is_negative1_or_positive])
    credit_mix = IntegerField(validators= [is_positive])
    class Meta:
        model = Customer
        fields = (
            "first_name",
            "last_name",
            "email",
            "mobile_number",
            "date_of_birth",
            "id_front",
            "id_back",
            "current_debt_outside", 
            "credit_limit_outside",  
            "credit_history_length",
            "pursuit_of_new_credit",
            "months_since_last_late_payment", 
            "credit_mix"  
        )
        read_only_fields = ("user_type", "usercode","password")

    def create(self, validated_data):
        validated_data["user_type"] = USER_TYPE.CUSTOMER  
        email = validated_data.get('email')
        username_token = hashlib.sha256(email.encode()).hexdigest()  # Generate username token
        validated_data["usercode"] = username_token
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance 
    
class VerifyEmailSerializer(Serializer):
    'Serializer to validate the customer, activate the account and set a password'
    usercode = CharField()
    password = CharField()
    new_password1 = CharField()
    new_password2 = CharField()

    def validate(self, attrs):
        usercode = attrs.get('usercode')
        password = attrs.get('password')
        new_password1 = attrs.get('new_password1')
        new_password2 = attrs.get('new_password2')

        customer = get_customer_by_usercode(usercode)

        if not customer:
            raise ValidationError('Invalid usercode')
        
        if customer.is_active:
            raise ValidationError('Account already activated')
        
        if not customer.check_password(password):
            print(customer.password)
            raise ValidationError('Invalid password')

        if new_password1 != new_password2:
            raise ValidationError("New passwords don't match")
        

        return attrs

    def update_customer(self, validated_data):
        usercode = validated_data.get('usercode')
        new_password = validated_data.get('new_password1')

        customer =get_customer_by_usercode(usercode)
        customer.password = make_password(new_password)
        customer.is_active = True
        customer.save()

        return customer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Override TokenObtainPairSerializer to add extra responses"""
    username_field = get_user_model().USERNAME_FIELD
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        if hasattr(user, "permission"):
            token["permission"] = user.permission
        return token
    def validate(self, attrs: Any) -> Dict[str, Any]:
        data = {}
        self.user = get_user_by_email(attrs["email"])
        if self.user is None:
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )
        if not self.user.is_active:
            raise exceptions.AuthenticationFailed(
                self.error_messages["this email is not activated"],
                "this email is not activated",)
        
        if check_password(attrs.get("password"), self.user.password):
            return self.custom_token(data)
        raise exceptions.AuthenticationFailed(
            self.error_messages["no_active_account"],
            "no_active_account",
        )

    def custom_token(self, data: Dict):
        refresh = self.get_token(self.user)
        data["refresh_token"] = str(refresh)
        data["access_token"] = str(refresh.access_token)
        data["email"] = self.user.email
        data["user_type"] = self.user.user_type
        return data
    
 


class MyTokenRefreshSerializer(TokenRefreshSerializer):
    """serializer to refresh user token"""

    def validate(self, attrs: Any) -> Dict[str, Any]:
        data = super().validate(attrs)
        decoded_payload = token_backend.decode(data["access"], verify=True)
        user_id = decoded_payload["user_id"]
        user = get_user_by_id(user_id)
        refresh = RefreshToken.for_user(user)
        data["refresh"] = str(refresh)
        return data

# class ChangePasswordSerializer(Serializer):
#     new_password = CharField()
#     verify_new_password = CharField()


# class AdminRegisterSerializer(ModelSerializer):
#     """class RegisterSerializer to serialize the user obj"""
 
#     class Meta:
#         model = MyUser
#         fields = (
#             "first_name",
#             "last_name",
#             "email",
#             "password",
#             "mobile_number",  
#             "user_type",
             
#         )

#     def create(self, validated_data):
#         password = validated_data.pop("password", None)
#         instance = self.Meta.model(**validated_data)
#         if password is not None:
#             instance.set_password(password)
#         instance.save()
#         return instance
    
# class MerchantRegisterSerializer(ModelSerializer):
#     """class RegisterSerializer to serialize the user obj"""
 
#     class Meta:
#         model = MyUser
#         fields = (
#             "first_name",
#             "last_name",
#             "email",
#             "password",
#             "mobile_number",  
#             "user_type",
#             "business"
             
#         )

#     def create(self, validated_data):
#         password = validated_data.pop("password", None)
#         instance = self.Meta.model(**validated_data)
#         if password is not None:
#             instance.set_password(password)
#         instance.save()
#         return instance
