from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from app.DTO.RegisterDTO import RegisterDTO
from app.Providers import container
from app.Services.Contracts.AuthService import AuthService


class AuthController(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
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
