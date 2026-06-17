from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.Authentication.JWTAuthentication import AppJWTAuthentication
from app.DTO.ChatDTO import ChatCreateDTO, ChatMessageCreateDTO, ChatUpdateDTO
from app.Providers import container
from app.Services.Contracts.ChatService import ChatService


class ChatController(APIView):
    authentication_classes = [AppJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id: int | None = None, message_id: int | None = None):
        service = container.resolve(ChatService)
        user_id = request.user.id

        if id is None:
            return Response(
                {
                    "error": False,
                    "status": "success",
                    "data": service.list(user_id),
                },
                status=status.HTTP_200_OK,
            )

        if message_id is not None:
            return Response(
                {
                    "error": False,
                    "status": "success",
                    "data": service.get_message_detail(id, user_id, message_id),
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {
                "error": False,
                "status": "success",
                "data": service.get_detail(id, user_id),
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request, id: int | None = None, message_id: int | None = None):
        service = container.resolve(ChatService)
        user_id = request.user.id

        if id is not None:
            dto = ChatMessageCreateDTO.from_request(request.data, request.FILES)
            return Response(
                {
                    "error": False,
                    "status": "success",
                    "data": service.send_message(id, user_id, dto),
                },
                status=status.HTTP_201_CREATED,
            )

        dto = ChatCreateDTO.from_request(request.data)
        return Response(
            {
                "error": False,
                "status": "success",
                "data": service.create(user_id, dto),
            },
            status=status.HTTP_201_CREATED,
        )

    def put(self, request, id: int):
        service = container.resolve(ChatService)
        dto = ChatUpdateDTO.from_request(request.data)
        return Response(
            {
                "error": False,
                "status": "success",
                "data": service.update(id, request.user.id, dto),
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, id: int):
        service = container.resolve(ChatService)
        service.delete(id, request.user.id)
        return Response(
            {
                "error": False,
                "status": "success",
                "data": True,
            },
            status=status.HTTP_200_OK,
        )
