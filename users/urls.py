from django.urls import path

from . import views


app_name = "users"
urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("profile/", views.profile_view, name="profile"),
    path("address/", views.address_view, name="address"),
]
