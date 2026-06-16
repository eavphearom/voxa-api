from app.Repositories.Contracts.UserRepository import UserRepository
from app.Repositories.UserRepositoryImpl import UserRepositoryImpl
from app.Repositories.Contracts.ChatRepository import ChatRepository
from app.Repositories.ChatRepositoryImpl import ChatRepositoryImpl
from app.Repositories.Contracts.ChatMessageRepository import ChatMessageRepository
from app.Repositories.ChatMessageRepositoryImpl import ChatMessageRepositoryImpl


REPOSITORY_BINDINGS = {
    UserRepository: lambda container: UserRepositoryImpl(),
    ChatRepository: ChatRepositoryImpl,
    ChatMessageRepository: ChatMessageRepositoryImpl,
}
