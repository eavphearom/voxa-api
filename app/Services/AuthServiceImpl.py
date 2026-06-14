from typing import Any

from django.contrib.auth.hashers import check_password, make_password
from rest_framework_simplejwt.tokens import AccessToken

from app.DTO.LoginDTO import LoginDTO
from app.DTO.RegisterDTO import RegisterDTO
from app.Enums import Role
from app.Exceptions import ValidationException
from app.Repositories.Contracts.UserRepository import UserRepository
from app.Services.Contracts.AuthService import AuthService


class AuthServiceImpl(AuthService):
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def register(self, dto: RegisterDTO) -> dict[str, Any]:
        self._validate_register_data(dto)

        created_user = self.user_repository.create(
            {
                "name": dto.name.strip(),
                "email": dto.email.strip().lower(),
                "phone": dto.phone.strip(),
                "password": make_password(dto.password),
                "role": Role.USER.value,
            }
        )
        return True
        # return {
        #     "id": created_user.id,
        #     "name": created_user.name,
        #     "email": created_user.email,
        #     "phone": created_auser.phone,
        #     "role": created_user.role,
        #     "token": "",
        #     "profile": created_user.avatar or "",
        # }

    def login(self, dto: LoginDTO) -> dict[str, Any]:
        self._validate_login_data(dto)
        user = self.user_repository.find_by_email(dto.email.strip().lower())

        if user is None or not check_password(dto.password, user.password):
            raise ValidationException("Invalid email or password")

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "role": user.role,
            "token": str(AccessToken.for_user(user)),
            "profile": user.avatar or "",
        }

    def logout(self, request) -> bool:
        return True

    def _validate_register_data(self, dto: RegisterDTO) -> None:
        if not dto.name or not dto.name.strip():
            raise ValidationException("Name is required")
        if not dto.email or not dto.email.strip():
            raise ValidationException("Email is required")
        if not dto.phone or not dto.phone.strip():
            raise ValidationException("Phone is required")
        if not dto.password:
            raise ValidationException("Password is required")
        if len(dto.password) < 6:
            raise ValidationException("Password must be at least 6 characters")
        if self.user_repository.find_by_email(dto.email.strip().lower()) is not None:
            raise ValidationException("Email already exists")
        if self.user_repository.find_by_phone(dto.phone.strip()) is not None:
            raise ValidationException("Phone already exists")

    def _validate_login_data(self, dto: LoginDTO) -> None:
        if not dto.email or not dto.email.strip():
            raise ValidationException("Email is required")
        if not dto.password:
            raise ValidationException("Password is required")
