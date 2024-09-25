from django.urls import path
from .views import RegisterUserview
from .views import VerifyUserEmail
from .views import LoginUserView
from .views import TestAuthenticationView
from .views import PasswordResetConfirmView
from .views import PasswordResetRequestView
from .views import SetNewPassword

urlpatterns = [
    path("register", RegisterUserview.as_view(), name="register"),
    path("verifyemail", VerifyUserEmail.as_view(), name="Verify email"),
    path("login/", LoginUserView.as_view(), name="login"),
    path("profile/", TestAuthenticationView.as_view(), name="granted"),
    path("password-reset/", PasswordResetRequestView.as_view(), name="password-reset"),
    path("password-reset-confirm/<uidb64>/<token>/",PasswordResetConfirmView.as_view(),name="password-reset-confirm",),
    path("set-new-password/", SetNewPassword.as_view(), name="set new password"),
]
  