from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from app.DTO.LoginDTO import LoginDTO
from app.DTO.RegisterDTO import RegisterDTO
from app.Exceptions import ValidationException
from app.Providers import container
from app.Services.Contracts.AuthService import AuthService


class AuthController(APIView):
    permission_classes = [AllowAny]
    action = "register"

    def post(self, request):
        if self.action == "login":
            return self.login(request)
        return self.register(request)

    def register(self, request):
        service = container.resolve(AuthService)

        dto = RegisterDTO(
            name=request.data.get("name", ""),
            email=request.data.get("email", ""),
            phone=request.data.get("phone", ""),
            password=request.data.get("password", ""),
        )

        data = service.register(dto)

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
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            raise

        return Response(
            {
                "error": False,
                "success": True,
                "message": "Login successfully",
                "data": data,
            },
            status=status.HTTP_200_OK,
        )
