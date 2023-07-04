from sqlite3 import Timestamp
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,AnonymousUser
from django.db import models
from typing import Any, Union
from django.contrib import admin
 
 


class USER_TYPE(models.TextChoices):
    """types of users"""

    # User-Admin
    ADMIN = "Admin", "admin"
    CUSTOMER = "Customer", "customer"
    MERCHANT= "Merchant", "merchant"

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True

        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    mobile_number = models.CharField(max_length=15)
    user_type = models.CharField(max_length=20, choices=USER_TYPE.choices)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = MyUserManager()
    USERNAME_FIELD = 'email'
    

    def __str__(self):
        return self.email

    @property
    def full_name(self) -> str:
        "return the user's full name"
        return "%s %s" % (self.first_name.title(), self.last_name.title())
    def has_perm(
        self, perm: str, obj: Union[models.Model, AnonymousUser, None] = None
    ) -> bool:
        """For checking permissions. to keep it simple all admin have ALL permissions"""
        return self.is_admin

    @staticmethod
    def has_module_perms(app_label: Any) -> bool:
        """Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)"""
        return True
admin.site.register(MyUser)