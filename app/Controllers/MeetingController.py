from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.DTO import MeetingCreateDTO, MeetingUpdateDTO
from app.Enums import MeetingStatus
from app.Providers import container
from app.Services.Contracts.MeetingService import MeetingService


class MeetingController(APIView):
    def get(self, request, meeting_id: int | None = None):
        service = container.resolve(MeetingService)
        if meeting_id is not None:
            return Response(service.get(meeting_id).to_dict())
        user_id = int(request.query_params.get("user_id"))
        return Response([meeting.to_dict() for meeting in service.list_by_user(user_id)])

    def post(self, request):
        service = container.resolve(MeetingService)
        dto = MeetingCreateDTO(
            user_id=int(request.data.get("user_id")),
            title=request.data.get("title", ""),
            description=request.data.get("description", ""),
            audio_file=request.FILES.get("audio_file"),
            duration=int(request.data.get("duration", 0)),
            language=request.data.get("language", ""),
        )
        return Response(service.create(dto).to_dict(), status=status.HTTP_201_CREATED)

    def patch(self, request, meeting_id: int):
        service = container.resolve(MeetingService)
        status_value = request.data.get("status")
        dto = MeetingUpdateDTO(
            title=request.data.get("title"),
            description=request.data.get("description"),
            duration=request.data.get("duration"),
            status=MeetingStatus(status_value) if status_value else None,
            language=request.data.get("language"),
        )
        return Response(service.update(meeting_id, dto).to_dict())
