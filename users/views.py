from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from verify_email.email_handler import send_verification_email

from .forms import CustomUserCreationForm, LoginForm, ProfileForm, AddressForm
from .models import Profile, Address


def home(request):
    return HttpResponse("Success")


def register_view(request):
    template_name = "users/register.html"
    registerForm = CustomUserCreationForm(request.POST or None)

    if request.method == "POST":
        if registerForm.is_valid():
            inactive_user = send_verification_email(request, registerForm)
            return redirect("users:login")

    context = {"registerForm": registerForm}

    return render(request, template_name, context)


@csrf_exempt
def login_view(request):
    template_name = "users/login.html"
    loginForm = LoginForm(request.POST or None)

    if request.method == "POST":
        if loginForm.is_valid():
            email = loginForm.cleaned_data["email"]
            password = loginForm.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect(reverse("users:home"), permanent=True)
            else:
                return HttpResponse("Email or password is wrong...")

    context = {"loginForm": loginForm}

    return render(request, template_name, context)


@login_required
def profile_view(request):
    template_name = "users/profile.html"

    if request.user.is_authenticated:
        profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        profileForm = ProfileForm(request.POST, instance=profile)

        if profileForm.is_valid():
            profileForm.save()
            return redirect("users:login")

    else:
        profileForm = ProfileForm(instance=profile)

    return render(request, template_name, {"profileForm": profileForm})


def address_view(request):
    template_name = "users/address.html"

    if request.user.is_authenticated:
        address, created = Address.objects.get_or_create(user=request.user)

    if request.method == "POST":
        addressForm = AddressForm(request.POST, instance=address)

        if addressForm.is_valid():
            addressForm.save()
            return redirect("users:login")
    else:
        addressForm = AddressForm(instance=address)

    return render(request, template_name, {"addressForm": addressForm})
