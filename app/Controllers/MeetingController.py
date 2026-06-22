from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.Authentication.JWTAuthentication import AppJWTAuthentication
from app.DTO.MeetingDTO import MeetingImportDTO, MeetingRecordStartDTO
from app.DTO.meeting_dtos import MeetingListFilterDTO
from app.Providers import container
from app.Services.Contracts.MeetingService import MeetingService


class MeetingController(APIView):
    authentication_classes = [AppJWTAuthentication]
    permission_classes = [IsAuthenticated]
    action = None

    def get(self, request, id: int | None = None):
        service = container.resolve(MeetingService)
        user_id = request.user.id

        if id is None:
            return Response(
                {
                    "error": False,
                    "status": "OK",
                    "data": service.list(
                        user_id,
                        MeetingListFilterDTO.from_query_params(request.query_params),
                    ),
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {
                "error": False,
                "status": "OK",
                "data": service.get_detail(id, user_id),
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request, id: int | None = None):
        if self.action == "import_meeting":
            return self.import_meeting(request)
        if self.action == "record_start":
            return self.start_recording(request)
        if self.action == "record_chunk":
            return self.record_chunk(request, id)
        if self.action == "record_finish":
            return self.finish_recording(request, id)

        return Response(
            {
                "error": True,
                "status": "error",
                "message": "Unsupported meeting action",
                "data": None,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, id: int):
        service = container.resolve(MeetingService)
        service.delete(id, request.user.id)
        return Response(
            {
                "error": False,
                "status": "success",
                "message": "Meeting deleted successfully",
                "data": True,
            },
            status=status.HTTP_200_OK,
        )

    def import_meeting(self, request):
        service = container.resolve(MeetingService)
        dto = MeetingImportDTO.from_request(request.data, request.FILES)
        data = service.import_meeting(request.user.id, dto)

        return Response(
            {
                "error": False,
                "status": "OK",
                "message": "Meeting uploaded successfully",
                "data": data,
            },
            status=status.HTTP_201_CREATED,
        )

    def start_recording(self, request):
        service = container.resolve(MeetingService)
        dto = MeetingRecordStartDTO.from_request(request.data)
        return Response(
            {
                "error": False,
                "status": "OK",
                "message": "Recording meeting started",
                "data": service.start_recording(request.user.id, dto),
            },
            status=status.HTTP_201_CREATED,
        )

    def record_chunk(self, request, meeting_id: int):
        service = container.resolve(MeetingService)
        chunk = request.FILES.get("chunk") or request.FILES.get("audio_chunk")
        return Response(
            {
                "error": False,
                "status": "OK",
                "data": service.transcribe_recording_chunk(meeting_id, request.user.id, chunk),
            },
            status=status.HTTP_200_OK,
        )

    def finish_recording(self, request, meeting_id: int):
        service = container.resolve(MeetingService)
        source_file = request.FILES.get("file") or request.FILES.get("recording")
        return Response(
            {
                "error": False,
                "status": "OK",
                "message": "Recording queued for processing",
                "data": service.finish_recording(meeting_id, request.user.id, source_file),
            },
            status=status.HTTP_202_ACCEPTED,
        )
