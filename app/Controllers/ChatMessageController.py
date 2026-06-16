from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.DTO.ChatMessageDTO import ChatMessageDTO
from app.Providers import container
from app.Services.Contracts.ChatMessageService import ChatMessageService


class ChatMessageController(APIView):
    def get(self, request, id: int | None = None):
        service = container.resolve(ChatMessageService)
        if id is None:
            return self.index(service)
        return self.show(service, id)

    def post(self, request):
        service = container.resolve(ChatMessageService)
        return self.create(service, request)

    def put(self, request, id: int):
        service = container.resolve(ChatMessageService)
        return self.update(service, request, id)

    def delete(self, request, id: int):
        service = container.resolve(ChatMessageService)
        return self.delete_item(service, id)

    def index(self, service):
        return Response(service.get_all())

    def show(self, service, id: int):
        return Response(service.get_by_id(id))

    def create(self, service, request):
        dto = ChatMessageDTO.from_request(request.data)
        return Response(service.create(dto), status=status.HTTP_201_CREATED)

    def update(self, service, request, id: int):
        dto = ChatMessageDTO.from_request(request.data)
        return Response(service.update(id, dto))

    def delete_item(self, service, id: int):
        service.delete(id)
        return Response(status=status.HTTP_204_NO_CONTENT)
