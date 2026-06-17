from django.urls import path

from app.Controllers.AuthController import AuthController
from app.Controllers.ChatController import ChatController
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
    path("meetings", MeetingController.as_view(), name="meetings-index"),
    path("meetings/<int:id>", MeetingController.as_view(), name="meetings-show"),
    path("meetings/create", MeetingController.as_view(), name="meetings-create"),
    path("meetings/<int:id>/update", MeetingController.as_view(), name="meetings-update"),
    path("meetings/<int:id>/delete", MeetingController.as_view(), name="meetings-delete"),
    # End Meeting routes
]
