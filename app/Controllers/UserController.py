from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from app.Authentication.JWTAuthentication import AppJWTAuthentication
from app.DTO.user_dtos import UserUpdateDTO
from app.Exceptions import NotFoundException, ValidationException
from app.Helpers.file_url import build_file_url
from app.Providers import container
from app.Services.Contracts.UserService import UserService


class UserController(APIView):
    authentication_classes = [AppJWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        service = container.resolve(UserService)
        try:
            data = service.get_profile(request.user.id)
        except NotFoundException as exc:
            return self._error(str(exc), status.HTTP_404_NOT_FOUND)

        self._add_avatar_url(request, data)
        return Response(
            {
                "error": False,
                "success": True,
                "message": "Profile retrieved successfully",
                "data": data,
            },
            status=status.HTTP_200_OK,
        )

    def patch(self, request):
        service = container.resolve(UserService)

        try:
            dto = UserUpdateDTO.from_data(request.data, request.FILES)
            data = service.update_profile(request.user.id, dto)
        except ValidationException as exc:
            return self._error(str(exc), status.HTTP_400_BAD_REQUEST)
        except NotFoundException as exc:
            return self._error(str(exc), status.HTTP_404_NOT_FOUND)

        self._add_avatar_url(request, data)
        return Response(
            {
                "error": False,
                "success": True,
                "message": "Profile updated successfully",
                "data": data,
            },
            status=status.HTTP_200_OK,
        )

    @staticmethod
    def _error(message: str, response_status: int) -> Response:
        return Response(
            {
                "error": True,
                "success": False,
                "message": message,
                "data": None,
            },
            status=response_status,
        )

    @staticmethod
    def _add_avatar_url(request, data: dict) -> None:
        avatar_url = build_file_url(request, data.get("avatar") or data.get("profile"))
        data["avatar"] = avatar_url
        data["profile"] = avatar_url
