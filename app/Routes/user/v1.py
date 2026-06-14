from django.urls import path

from app.Controllers.AuthController import AuthController
from app.Controllers.LoginController import LoginController


urlpatterns = [
    path("auth/register", AuthController.as_view(), name="auth-register"),
    path("auth/login", LoginController.as_view(), name="auth-login"),
]
