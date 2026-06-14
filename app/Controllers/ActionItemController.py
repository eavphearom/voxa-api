from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.DTO import ActionItemCreateDTO, ActionItemUpdateDTO
from app.Enums import ActionItemStatus
from app.Providers import container
from app.Services.Contracts import ActionItemServiceContract


class ActionItemController(APIView):
    def get(self, request):
        service = container.resolve(ActionItemServiceContract)
        meeting_id = int(request.query_params.get("meeting_id"))
        return Response([item.to_dict() for item in service.list_by_meeting(meeting_id)])

    def post(self, request):
        service = container.resolve(ActionItemServiceContract)
        dto = ActionItemCreateDTO(
            meeting_id=int(request.data.get("meeting_id")),
            content=request.data.get("content", ""),
            status=ActionItemStatus(request.data.get("status", ActionItemStatus.PENDING.value)),
        )
        return Response(service.create(dto).to_dict(), status=status.HTTP_201_CREATED)

    def patch(self, request, action_item_id: int):
        service = container.resolve(ActionItemServiceContract)
        status_value = request.data.get("status")
        dto = ActionItemUpdateDTO(
            content=request.data.get("content"),
            status=ActionItemStatus(status_value) if status_value else None,
        )
        return Response(service.update(action_item_id, dto).to_dict())
