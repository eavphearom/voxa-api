from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.DTO import ChatMessageCreateDTO, ChatSessionCreateDTO, ChatSessionUpdateDTO
from app.Enums import ChatRole
from app.Providers import container
from app.Services.Contracts import ChatServiceContract


class ChatSessionController(APIView):
    def get(self, request):
        service = container.resolve(ChatServiceContract)
        meeting_id = int(request.query_params.get("meeting_id"))
        return Response([session.to_dict() for session in service.list_by_meeting(meeting_id)])

    def post(self, request):
        service = container.resolve(ChatServiceContract)
        dto = ChatSessionCreateDTO(
            meeting_id=int(request.data.get("meeting_id")),
            user_id=int(request.data.get("user_id")),
            title=request.data.get("title", ""),
        )
        return Response(service.create_session(dto).to_dict(), status=status.HTTP_201_CREATED)

    def patch(self, request, session_id: int):
        service = container.resolve(ChatServiceContract)
        dto = ChatSessionUpdateDTO(title=request.data.get("title"))
        return Response(service.update_session(session_id, dto).to_dict())


class ChatMessageController(APIView):
    def post(self, request):
        service = container.resolve(ChatServiceContract)
        dto = ChatMessageCreateDTO(
            chat_session_id=int(request.data.get("chat_session_id")),
            role=ChatRole(request.data.get("role", ChatRole.USER.value)),
            message=request.data.get("message", ""),
        )
        return Response(service.add_message(dto).to_dict(), status=status.HTTP_201_CREATED)
