from app.Repositories.Contracts.UserRepository import UserRepository
from app.Services.AuthServiceImpl import AuthServiceImpl
from app.Services.Contracts.AuthService import AuthService


SERVICE_BINDINGS = {
    AuthService: lambda container: AuthServiceImpl(container.resolve(UserRepository)),
}
