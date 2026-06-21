from django.urls import path

from app.Controllers.AuthController import AuthController
from app.Controllers.ChatController import ChatController
from app.Controllers.FolderController import FolderController
from app.Controllers.MeetingController import MeetingController


urlpatterns = [
    path("auth/register", AuthController.as_view(), name="auth-register"),
    path("auth/login", AuthController.as_view(action="login"), name="auth-login"),
    path("auth/logout", AuthController.as_view(action="logout"), name="auth-logout"),
    # Chat routes
    path("chats", ChatController.as_view(), name="chats-index"),
    path("chats/<int:id>", ChatController.as_view(), name="chats-show"),
    path("chats/<int:id>/messages", ChatController.as_view(), name="chats-messages-create"),
    path("chats/<int:id>/messages/<int:message_id>", ChatController.as_view(), name="chats-messages-show"),
    # End Chat routes
    # Meeting routes
    path("meetings/import", MeetingController.as_view(action="import_meeting"), name="meetings-import"),
    path("meetings/record/start", MeetingController.as_view(action="record_start"), name="meetings-record-start"),
    path(
        "meetings/<int:id>/record/chunk",
        MeetingController.as_view(action="record_chunk"),
        name="meetings-record-chunk",
    ),
    path(
        "meetings/<int:id>/record/finish",
        MeetingController.as_view(action="record_finish"),
        name="meetings-record-finish",
    ),
    path("meetings", MeetingController.as_view(), name="meetings-index"),
    path("meetings/<int:id>", MeetingController.as_view(), name="meetings-show"),
    # End Meeting routes
    # Folder routes
    path("folders", FolderController.as_view(), name="folders-index"),
    path("folders/<int:id>", FolderController.as_view(), name="folders-show"),
    path("folders/<int:id>/meetings", FolderController.as_view(action="meetings"), name="folders-meetings"),
    path(
        "folders/<int:id>/meetings/<int:meeting_id>",
        FolderController.as_view(action="meeting"),
        name="folders-meeting",
    ),
    # End Folder routes
]
