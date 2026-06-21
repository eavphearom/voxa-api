from app.Repositories.Contracts.UserRepository import UserRepository
from app.Repositories.UserRepositoryImpl import UserRepositoryImpl
from app.Repositories.Contracts.ChatRepository import ChatRepository
from app.Repositories.ChatRepositoryImpl import ChatRepositoryImpl
from app.Repositories.Contracts.ChatMessageRepository import ChatMessageRepository
from app.Repositories.ChatMessageRepositoryImpl import ChatMessageRepositoryImpl
from app.Repositories.Contracts.ChatMessageAttachmentRepository import ChatMessageAttachmentRepository
from app.Repositories.ChatMessageAttachmentRepositoryImpl import ChatMessageAttachmentRepositoryImpl
from app.Repositories.Contracts.FolderRepository import FolderRepository
from app.Repositories.FolderRepositoryImpl import FolderRepositoryImpl
from app.Repositories.Contracts.MeetingRepository import MeetingRepository
from app.Repositories.MeetingRepositoryImpl import MeetingRepositoryImpl


REPOSITORY_BINDINGS = {
    UserRepository: lambda container: UserRepositoryImpl(),
    ChatRepository: ChatRepositoryImpl,
    ChatMessageRepository: ChatMessageRepositoryImpl,
    ChatMessageAttachmentRepository: ChatMessageAttachmentRepositoryImpl,
    FolderRepository: FolderRepositoryImpl,
    MeetingRepository: MeetingRepositoryImpl,
}
