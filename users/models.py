from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.conf import settings

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model
    """

    email = models.EmailField(unique=True, verbose_name="Email address", max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = "User"

    def __str__(self):
        return self.email
