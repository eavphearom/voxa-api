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
from app.Repositories.Contracts.FolderRepository import FolderRepository
from app.Services.Contracts.FolderService import FolderService
from app.Services.FolderServiceImpl import FolderServiceImpl
from app.Repositories.Contracts.MeetingRepository import MeetingRepository
from app.Services.Contracts.MeetingService import MeetingService
from app.Services.MeetingServiceImpl import MeetingServiceImpl
from app.Services.Contracts.MeetingJobService import MeetingJobService
from app.Services.MeetingJobServiceImpl import MeetingJobServiceImpl
from app.Services.Contracts.MeetingProcessingService import MeetingProcessingService
from app.Services.MeetingProcessingServiceImpl import MeetingProcessingServiceImpl
from app.Services.Contracts.MeetingTranscriptionService import MeetingTranscriptionService
from app.Services.MeetingTranscriptionServiceImpl import MeetingTranscriptionServiceImpl
from app.Services.Contracts.SpeakerDiarizationService import SpeakerDiarizationService
from app.Services.SpeakerDiarizationServiceImpl import SpeakerDiarizationServiceImpl


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
    FolderService: lambda container: FolderServiceImpl(
        container.resolve(FolderRepository),
        container.resolve(MeetingRepository),
    ),
    MeetingService: lambda container: MeetingServiceImpl(
        container.resolve(MeetingRepository),
        container.resolve(ChatRepository),
        container.resolve(ChatMessageRepository),
        container.resolve(MeetingJobService),
        container.resolve(MeetingTranscriptionService),
    ),
    MeetingJobService: lambda container: MeetingJobServiceImpl(),
    MeetingProcessingService: lambda container: MeetingProcessingServiceImpl(
        container.resolve(MeetingRepository),
        container.resolve(ChatRepository),
        container.resolve(ChatMessageRepository),
        container.resolve(MeetingTranscriptionService),
    ),
    MeetingTranscriptionService: lambda container: MeetingTranscriptionServiceImpl(
        container.resolve(SpeakerDiarizationService),
    ),
    SpeakerDiarizationService: lambda container: SpeakerDiarizationServiceImpl(),
}
