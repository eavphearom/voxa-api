import re
from typing import Any

from django.contrib.auth.hashers import check_password, make_password
from django.conf import settings
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import validate_email
from django.db import IntegrityError
from django.utils import timezone
from google.auth.exceptions import TransportError
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2 import id_token as google_id_token
from rest_framework_simplejwt.tokens import AccessToken

from app.DTO.GoogleLoginDTO import GoogleLoginDTO
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

        try:
            created_user = self.user_repository.create(
                {
                    "name": dto.name.strip(),
                    "email": dto.email.strip().lower(),
                    "phone": dto.phone.strip(),
                    "password": make_password(dto.password),
                    "role": Role.USER.value,
                }
            )
        except IntegrityError as exc:
            raise ValidationException("Email or phone already exists") from exc

        return {
            "id": created_user.id,
            "name": created_user.name,
            "email": created_user.email,
            "phone": created_user.phone,
            "role": created_user.role,
            "token": "",
            "profile": created_user.avatar or "",
        }

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

    def google_login(self, dto: GoogleLoginDTO) -> dict[str, Any]:
        if not dto.id_token or not dto.id_token.strip():
            raise ValidationException("Google ID token is required")
        if not settings.GOOGLE_CLIENT_ID:
            raise ValidationException("Google authentication is not configured")

        try:
            token_data = google_id_token.verify_oauth2_token(
                dto.id_token.strip(),
                GoogleRequest(),
                settings.GOOGLE_CLIENT_ID,
            )
        except TransportError as exc:
            raise ValidationException("Google token verification failed") from exc
        except ValueError as exc:
            message = str(exc).lower()
            if "expired" in message:
                raise ValidationException("Google ID token has expired") from exc
            raise ValidationException("Invalid Google ID token") from exc

        google_id = str(token_data.get("sub", "")).strip()
        email = str(token_data.get("email", "")).strip().lower()
        if not google_id or not email:
            raise ValidationException("Google ID token is missing required profile data")
        if token_data.get("email_verified") is not True:
            raise ValidationException("Google account email is not verified")

        user = self.user_repository.find_by_google_id(google_id)
        if user is None:
            user = self.user_repository.find_by_email(email)

        profile_data = {
            "google_id": google_id,
            "avatar": str(token_data.get("picture", "")).strip() or None,
            "email_verified_at": timezone.now(),
        }

        if user is None:
            try:
                user = self.user_repository.create(
                    {
                        "name": str(token_data.get("name", "")).strip() or email.split("@", 1)[0],
                        "email": email,
                        "phone": None,
                        "password": None,
                        "role": Role.USER.value,
                        **profile_data,
                    }
                )
            except IntegrityError as exc:
                raise ValidationException("Unable to create Google user") from exc
        else:
            user = self.user_repository.update(user, profile_data)

        return {
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "phone": user.phone,
                "role": user.role,
                "google_id": user.google_id,
                "profile": user.avatar or "",
            },
            "access_token": str(AccessToken.for_user(user)),
        }

    def logout(self, request) -> bool:
        return True

    def _validate_register_data(self, dto: RegisterDTO) -> None:
        if not dto.name or not dto.name.strip():
            raise ValidationException("Name is required")
        if not dto.email or not dto.email.strip():
            raise ValidationException("Email is required")
        try:
            validate_email(dto.email.strip())
        except DjangoValidationError as exc:
            raise ValidationException("Email format is invalid") from exc
        if not dto.phone or not dto.phone.strip():
            raise ValidationException("Phone is required")
        if not re.fullmatch(r"\+?[0-9]{8,20}", dto.phone.strip()):
            raise ValidationException("Phone must contain 8 to 20 digits")
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
