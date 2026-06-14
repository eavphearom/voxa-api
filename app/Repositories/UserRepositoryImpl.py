from app.model import User
from app.Repositories.Contracts.UserRepository import UserRepository


class UserRepositoryImpl(UserRepository):
    def find_by_email(self, email: str) -> User | None:
        return User.objects.filter(email=email).first()

    def find_by_phone(self, phone: str) -> User | None:
        return User.objects.filter(phone=phone).first()

    def create(self, user: User) -> User:
        user.save()
        return user
