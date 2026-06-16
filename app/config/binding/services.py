from app.Repositories.Contracts.UserRepository import UserRepository
from app.Services.AuthServiceImpl import AuthServiceImpl
from app.Services.Contracts.AuthService import AuthService
from app.Repositories.Contracts.ChatRepository import ChatRepository
from app.Services.Contracts.ChatService import ChatService
from app.Services.ChatServiceImpl import ChatServiceImpl
from app.Repositories.Contracts.ChatMessageRepository import ChatMessageRepository
from app.Services.Contracts.ChatMessageService import ChatMessageService
from app.Services.ChatMessageServiceImpl import ChatMessageServiceImpl
from app.Services.Contracts.GeminiService import GeminiService
from app.Services.GeminiServiceImpl import GeminiServiceImpl


SERVICE_BINDINGS = {
    AuthService: lambda container: AuthServiceImpl(container.resolve(UserRepository)),
    ChatService: lambda container: ChatServiceImpl(
        container.resolve(ChatRepository),
        container.resolve(ChatMessageRepository),
        container.resolve(GeminiService),
    ),
    ChatMessageService: lambda container: ChatMessageServiceImpl(container.resolve(ChatMessageRepository)),
    GeminiService: lambda container: GeminiServiceImpl(),
}
