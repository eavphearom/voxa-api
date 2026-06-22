from app.model import User
from app.Repositories.Contracts.UserRepository import UserRepository


class UserRepositoryImpl(UserRepository):
    def create(self, data: dict) -> User:
        return User.objects.create(**data)

    def find_by_email(self, email: str) -> User | None:
        return User.objects.filter(email=email).first()

    def find_by_google_id(self, google_id: str) -> User | None:
        return User.objects.filter(google_id=google_id).first()

    def find_by_phone(self, phone: str) -> User | None:
        return User.objects.filter(phone=phone).first()

    def find_by_id(self, user_id: int) -> User | None:
        return User.objects.filter(id=user_id).first()

    def update(self, user: User, data: dict) -> User:
        for field, value in data.items():
            setattr(user, field, value)
        user.save(update_fields=[*data.keys(), "updated_at"])
        return user
