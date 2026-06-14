from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from app.DTO.LoginDTO import LoginDTO
from app.Exceptions import ValidationException
from app.Providers import container
from app.Services.Contracts.AuthService import AuthService


class LoginController(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
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
