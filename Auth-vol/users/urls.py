from django.shortcuts import render
from .views import Register
from .views import LoginView
from .views import ProtectedView

from django.urls import path


urlpatterns = [
    path("register/", Register.as_view(), name="register"),
    path("login", LoginView.as_view(), name="login"),
    path("protected", ProtectedView.as_view(), name="protected"),
]
