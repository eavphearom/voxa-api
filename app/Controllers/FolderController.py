from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.DTO import FolderCreateDTO, FolderUpdateDTO
from app.Providers import container
from app.Services.Contracts import FolderServiceContract


class FolderController(APIView):
    def get(self, request):
        service = container.resolve(FolderServiceContract)
        user_id = int(request.query_params.get("user_id"))
        return Response([folder.to_dict() for folder in service.list_by_user(user_id)])

    def post(self, request):
        service = container.resolve(FolderServiceContract)
        dto = FolderCreateDTO(
            user_id=int(request.data.get("user_id")),
            name=request.data.get("name", ""),
        )
        return Response(service.create(dto).to_dict(), status=status.HTTP_201_CREATED)

    def patch(self, request, folder_id: int):
        service = container.resolve(FolderServiceContract)
        dto = FolderUpdateDTO(name=request.data.get("name"))
        return Response(service.update(folder_id, dto).to_dict())
