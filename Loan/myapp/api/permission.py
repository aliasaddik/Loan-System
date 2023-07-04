from rest_framework import permissions
from django.core.exceptions import PermissionDenied
from rest_framework.request import Request
from Loan.myapp.services.users import get_user_type_by_id
from Loan.myapp.models.users import USER_TYPE
from rest_framework.views import APIView
from Loan.myapp.models.users import MyUser


class UserIsAuthenticated(permissions.BasePermission):
    """
    logged in permission
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.user.is_authenticated and request.user.is_active:
            return True
        raise PermissionDenied


class IsAdmin(permissions.BasePermission):
    """
    admin permission
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.user.is_authenticated:
            userType = get_user_type_by_id(request.user.id)

            if userType == USER_TYPE.ADMIN:
                return True
            return False
        return False


class IsMerchant(permissions.BasePermission):
    """
    merchant permission
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.user.is_authenticated:
            userType = get_user_type_by_id(request.user.id)

            if userType == USER_TYPE.MERCHANT:

                return True
            return False
        return False


class IsCustomer(permissions.BasePermission):
    """
   customer user permission
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.user.is_authenticated:
            userType = get_user_type_by_id(request.user.id)
            if userType == USER_TYPE.CUSTOMER:
                return True
            return False
        return False


class CustomPermissions:
    """for check the type of user in views"""

    @staticmethod
    def admin_or_merchant(user: MyUser) -> bool:
        """return True only if the user is a merchant or admin"""
        return (
            True
            if user.user_type == USER_TYPE.ADMIN
            or user.user_type == USER_TYPE.MERCHANT
            else False
        )

    @staticmethod
    def admin(user: MyUser) -> bool:
        """return True only if the user is an admin"""
        return True if user.user_type == USER_TYPE.ADMIN else False
