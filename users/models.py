from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from django.contrib.sessions.models import Session

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


class GuestUser(models.Model):
    session = models.OneToOneField(Session, on_delete=models.CASCADE)

    def __str__(self):
        return f"Session ID: {self.session.session_key}"

    @admin.display(description="Session Expiration Date")
    def get_session_expiration_date(self):
        """
        Return the session expiration date or 'Session Expired' if not available.
        """
        return self.session.expire_date or "Session Expired"


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="profile",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Last name (optional)"
    )
    mobile_number = PhoneNumberField(region="IN", max_length=13, unique=True)

    def __str__(self):
        return self.first_name.title()

    def get_last_name_or_empty(self):
        """
        Returns the last name if available, or an empty string if it's None.
        """
        return self.last_name or ""

    @admin.display(description="User Name")
    def display_fullname(self):
        return f"{self.first_name} {self.get_last_name_or_empty()}".title()


class Address(models.Model):
    STATE_CHOICES = (
        ("Andaman and Nicobar islands", "Andaman and Nicobar islands"),
        ("Andhra Pradesh", "Andhra Pradesh"),
        ("Arunacal Pradesh", "Arunacal Pradesh"),
        ("Assam", "Assam"),
        ("Bihar", "Bihar"),
        ("Chandigarh", "Chandigarh"),
        ("Chhattisgarh", "Chhattisgarh"),
        ("Dadra & Nagar Haveli & Daman & Diu", "Dadra & Nagar Haveli & Daman & Diu"),
        ("Goa", "Goa"),
        ("Gujarat", "Gujarat"),
        ("Haryana", "Haryana"),
        ("Delhi", "Delhi"),
        ("Himachal Pradesh", "Himachal Pradesh"),
        ("Jammu & Kashmir", "Jammu & Kashmir"),
        ("Jharkand", "Jharkand"),
        ("Karnataka", "Karnataka"),
        ("Kerala", "Kerala"),
        ("Lakshadweep", "Lakshadweep"),
        ("Madhya Pradesh", "Madhya Pradesh"),
        ("Maharashtra", "Maharashtra"),
        ("Manipur", "Manipur"),
        ("Meghalaya", "Meghalaya"),
        ("Mizoram", "Mizoram"),
        ("Nagaland", "Nagaland"),
        ("Odisha", "Odisha"),
        ("Puducherry", "Puducherry"),
        ("Punjab", "Punjab"),
        ("Rajasthan", "Rajasthan"),
        ("Sikkim", "Sikkim"),
        ("Tamil Nadu", "Tamil Nadu"),
        ("Telanga", "Telanga"),
        ("Tripura", "Tripura"),
        ("Uttarkhand", "Uttarkhand"),
        ("Uttar Pradesh", "Uttar Pradesh"),
        ("West Bengal", "West Bengal"),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="address",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    guest_user = models.OneToOneField(
        GuestUser,
        related_name="guest_address",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=255)
    mobile_number = PhoneNumberField(region="IN", max_length=13, unique=True)
    pincode = models.CharField(max_length=6)
    address = models.TextField()
    city_district_town = models.CharField(
        max_length=255, verbose_name="City/District/Town"
    )
    state = models.CharField(choices=STATE_CHOICES, max_length=40)

    # Optional fields
    landmark = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Landmark (optional)"
    )
    alternate_phone = PhoneNumberField(
        region="IN",
        max_length=13,
        null=True,
        blank=True,
        verbose_name="Alternate Mobile Number (optional)",
    )

    class Meta:
        verbose_name = "User address"
        verbose_name_plural = "User addresses"

    def __str__(self):
        return self.name

    @admin.display(description="Is Guest")
    def is_guest(self):
        """
        Returns True if the address is associated with a guest user, otherwise False.
        """
        return self.guest_user is not None

    is_guest.boolean = True
