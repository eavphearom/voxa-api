from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.Authentication.JWTAuthentication import AppJWTAuthentication
from app.DTO.LoginDTO import LoginDTO
from app.DTO.GoogleLoginDTO import GoogleLoginDTO
from app.DTO.RegisterDTO import RegisterDTO
from app.Exceptions import ValidationException
from app.Helpers.file_url import build_file_url
from app.Providers import container
from app.Services.Contracts.AuthService import AuthService


class AuthController(APIView):
    authentication_classes = [AppJWTAuthentication]
    permission_classes = [AllowAny]
    action = "register"

    def get_permissions(self):
        if self.action == "logout":
            return [IsAuthenticated()]
        return [AllowAny()]

    def post(self, request):
        if self.action == "login":
            return self.login(request)
        if self.action == "google_login":
            return self.google_login(request)
        if self.action == "logout":
            return self.logout(request)
        return self.register(request)

    def register(self, request):
        service = container.resolve(AuthService)
        dto = RegisterDTO(
            name=request.data.get("name", ""),
            email=request.data.get("email", ""),
            phone=request.data.get("phone", ""),
            password=request.data.get("password", ""),
        )

        try:
            data = service.register(dto)
        except ValidationException as exc:
            return Response(
                {
                    "error": True,
                    "success": False,
                    "message": str(exc),
                    "data": None,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        data["profile"] = build_file_url(request, data.get("profile"))
        data["avatar"] = data["profile"]
        return Response(
            {
                "error": False,
                "success": True,
                "message": "Register successfully",
                "data": data,
            },
            status=status.HTTP_201_CREATED,
        )

    def login(self, request):
        service = container.resolve(AuthService)
        dto = LoginDTO(
            email=request.data.get("email", ""),
            password=request.data.get("password", ""),
        )

        try:
            data = service.login(dto)
        except ValidationException as exc:
            if str(exc) == "Invalid email or password":
                return Response(
                    {
                        "error": True,
                        "success": False,
                        "message": "Invalid email or password",
                        "data": None,
                    },
                    # Invalid credentials are a login-form validation error. Using
                    # 400 here also prevents global expired-token 401 handlers from
                    # replacing this message with "Unauthorized. Please login again."
                    status=status.HTTP_400_BAD_REQUEST,
                )
            raise

        data["profile"] = build_file_url(request, data.get("profile"))
        data["avatar"] = data["profile"]
        return Response(
            {
                "error": False,
                "success": True,
                "message": "Login successfully",
                "data": data,
            },
            status=status.HTTP_200_OK,
        )

    def google_login(self, request):
        service = container.resolve(AuthService)
        dto = GoogleLoginDTO(id_token=request.data.get("id_token", ""))

        try:
            data = service.google_login(dto)
        except ValidationException as exc:
            message = str(exc)
            response_status = status.HTTP_400_BAD_REQUEST
            if message == "Google token verification failed":
                response_status = status.HTTP_502_BAD_GATEWAY
            return Response(
                {
                    "error": True,
                    "success": False,
                    "message": message,
                    "data": None,
                },
                status=response_status,
            )

        user_data = data.get("user", {})
        user_data["profile"] = build_file_url(request, user_data.get("profile"))
        user_data["avatar"] = user_data["profile"]
        return Response(
            {
                "error": False,
                "success": True,
                "message": "Google login successful",
                "data": data,
            },
            status=status.HTTP_200_OK,
        )

    def logout(self, request):
        service = container.resolve(AuthService)
        data = service.logout(request)

        return Response(
            {
                "error": False,
                "status": "success",
                "message": "Logout successful.",
                "data": data,
            },
            status=status.HTTP_200_OK,
        )
