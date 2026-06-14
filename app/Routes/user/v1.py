from django.urls import path

from app.Controllers.AuthController import AuthController


urlpatterns = [
    path("auth/register", AuthController.as_view(), name="auth-register"),
    path("auth/login", AuthController.as_view(action="login"), name="auth-login"),
]
