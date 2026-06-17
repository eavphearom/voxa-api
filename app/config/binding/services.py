from app.Repositories.Contracts.UserRepository import UserRepository
from app.Services.AuthServiceImpl import AuthServiceImpl
from app.Services.Contracts.AuthService import AuthService
from app.Repositories.Contracts.ChatRepository import ChatRepository
from app.Services.Contracts.ChatService import ChatService
from app.Services.ChatServiceImpl import ChatServiceImpl
from app.Repositories.Contracts.ChatMessageRepository import ChatMessageRepository
from app.Services.Contracts.ChatMessageService import ChatMessageService
from app.Services.ChatMessageServiceImpl import ChatMessageServiceImpl
from app.Repositories.Contracts.ChatMessageAttachmentRepository import ChatMessageAttachmentRepository
from app.Services.Contracts.ChatMessageAttachmentService import ChatMessageAttachmentService
from app.Services.ChatMessageAttachmentServiceImpl import ChatMessageAttachmentServiceImpl
from app.Services.Contracts.ChatAttachmentContentService import ChatAttachmentContentService
from app.Services.ChatAttachmentContentServiceImpl import ChatAttachmentContentServiceImpl
from app.Services.Contracts.GeminiService import GeminiService
from app.Services.GeminiServiceImpl import GeminiServiceImpl
from app.Repositories.Contracts.MeetingRepository import MeetingRepository
from app.Services.Contracts.MeetingService import MeetingService
from app.Services.MeetingServiceImpl import MeetingServiceImpl


SERVICE_BINDINGS = {
    AuthService: lambda container: AuthServiceImpl(container.resolve(UserRepository)),
    ChatService: lambda container: ChatServiceImpl(
        container.resolve(ChatRepository),
        container.resolve(ChatMessageRepository),
        container.resolve(ChatMessageAttachmentService),
        container.resolve(ChatAttachmentContentService),
        container.resolve(GeminiService),
    ),
    ChatMessageService: lambda container: ChatMessageServiceImpl(container.resolve(ChatMessageRepository)),
    ChatMessageAttachmentService: lambda container: ChatMessageAttachmentServiceImpl(
        container.resolve(ChatMessageAttachmentRepository),
    ),
    ChatAttachmentContentService: lambda container: ChatAttachmentContentServiceImpl(),
    GeminiService: lambda container: GeminiServiceImpl(),
    MeetingService: lambda container: MeetingServiceImpl(container.resolve(MeetingRepository)),
}
