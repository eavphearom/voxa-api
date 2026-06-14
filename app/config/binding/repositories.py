from app.Repositories.Contracts.UserRepository import UserRepository
from app.Repositories.UserRepositoryImpl import UserRepositoryImpl


REPOSITORY_BINDINGS = {
    UserRepository: UserRepositoryImpl,
}
