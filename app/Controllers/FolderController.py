from __future__ import annotations

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.Authentication.JWTAuthentication import AppJWTAuthentication
from app.DTO.folder_dtos import FolderCreateDTO, FolderUpdateDTO
from app.Providers import container
from app.Services.Contracts.FolderService import FolderService


class FolderController(APIView):
    authentication_classes = [AppJWTAuthentication]
    permission_classes = [IsAuthenticated]
    action = None

    def get(self, request, id: int | None = None, meeting_id: int | None = None):
        service = container.resolve(FolderService)
        user_id = request.user.id
        if self.action == "meetings":
            return self._success(service.list_meetings(id, user_id))
        if id is None:
            return self._success(service.list(user_id))
        return self._success(service.get_detail(id, user_id))

    def post(self, request, id: int | None = None, meeting_id: int | None = None):
        service = container.resolve(FolderService)
        if self.action == "meeting":
            return self._success(
                service.add_meeting(id, meeting_id, request.user.id),
                status.HTTP_201_CREATED,
            )
        dto = FolderCreateDTO.from_request(request.data)
        return self._success(service.create(request.user.id, dto), status.HTTP_201_CREATED)

    def put(self, request, id: int):
        service = container.resolve(FolderService)
        dto = FolderUpdateDTO.from_request(request.data)
        return self._success(service.update(id, request.user.id, dto))

    def delete(self, request, id: int, meeting_id: int | None = None):
        service = container.resolve(FolderService)
        if self.action == "meeting":
            service.remove_meeting(id, meeting_id, request.user.id)
        else:
            service.delete(id, request.user.id)
        return self._success(True)

    def _success(self, data, response_status=status.HTTP_200_OK):
        return Response(
            {"error": False, "status": "success", "data": data},
            status=response_status,
        )
