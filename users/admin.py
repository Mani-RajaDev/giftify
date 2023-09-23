from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.sessions.models import Session

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import (
    CustomUser,
    GuestUser,
    Address,
    Profile,
)


# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    model = CustomUser

    list_display = ["email", "is_staff", "is_superuser"]
    list_filter = ["email", "is_staff"]

    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        (
            "Permissions",
            {"fields": ("is_staff", "is_active", "groups", "user_permissions")},
        ),
    ]

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )

    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []


@admin.register(GuestUser)
class GuestUserAdmin(admin.ModelAdmin):
    list_display = ["session", "get_session_expiration_date"]

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        "display_fullname",
        "mobile_number",
    ]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["__str__", "is_guest", "mobile_number", "state"]


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ["session_key", "expire_date"]