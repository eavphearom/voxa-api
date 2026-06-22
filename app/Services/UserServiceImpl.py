import re
from pathlib import Path
from typing import Any

from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.files.storage import default_storage
from django.core.validators import validate_email
from django.utils.text import get_valid_filename

from app.DTO.user_dtos import UserUpdateDTO
from app.Exceptions import NotFoundException, ValidationException
from app.Repositories.Contracts.UserRepository import UserRepository
from app.Services.Contracts.UserService import UserService


class UserServiceImpl(UserService):
    MAX_PROFILE_SIZE = 5 * 1024 * 1024
    ALLOWED_PROFILE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def get_profile(self, user_id: int) -> dict[str, Any]:
        user = self.user_repository.find_by_id(user_id)
        if user is None:
            raise NotFoundException("User not found")
        return self._to_dict(user)

    def update_profile(self, user_id: int, dto: UserUpdateDTO) -> dict[str, Any]:
        user = self.user_repository.find_by_id(user_id)
        if user is None:
            raise NotFoundException("User not found")

        update_data = self._validate_update_data(user_id, dto)
        if not update_data:
            raise ValidationException("At least one profile field is required")

        user = self.user_repository.update(user, update_data)
        return self._to_dict(user)

    @staticmethod
    def _to_dict(user) -> dict[str, Any]:
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "role": user.role,
            "google_id": user.google_id,
            "avatar": user.avatar or "",
            "profile": user.avatar or "",
        }

    def _validate_update_data(self, user_id: int, dto: UserUpdateDTO) -> dict[str, Any]:
        update_data: dict[str, Any] = {}

        if dto.name is not None:
            if not dto.name:
                raise ValidationException("Name is required")
            if len(dto.name) > 255:
                raise ValidationException("Name must not exceed 255 characters")
            update_data["name"] = dto.name

        if dto.email is not None:
            email = dto.email.lower()
            try:
                validate_email(email)
            except DjangoValidationError as exc:
                raise ValidationException("Email format is invalid") from exc
            existing_user = self.user_repository.find_by_email(email)
            if existing_user is not None and existing_user.id != user_id:
                raise ValidationException("Email already exists")
            update_data["email"] = email

        if dto.phone is not None:
            if not re.fullmatch(r"\+?[0-9]{8,20}", dto.phone):
                raise ValidationException("Phone must contain 8 to 20 digits")
            existing_user = self.user_repository.find_by_phone(dto.phone)
            if existing_user is not None and existing_user.id != user_id:
                raise ValidationException("Phone already exists")
            update_data["phone"] = dto.phone

        if dto.avatar is not None:
            update_data["avatar"] = dto.avatar or None

        if dto.profile_file is not None:
            update_data["avatar"] = self._store_profile_image(user_id, dto.profile_file)

        return update_data

    def _store_profile_image(self, user_id: int, uploaded_file) -> str:
        file_name = get_valid_filename(str(getattr(uploaded_file, "name", "")))
        extension = Path(file_name).suffix.lower()
        content_type = str(getattr(uploaded_file, "content_type", "")).lower()
        file_size = int(getattr(uploaded_file, "size", 0) or 0)

        if not file_name or extension not in self.ALLOWED_PROFILE_EXTENSIONS:
            raise ValidationException("Profile image must be JPG, PNG, or WEBP")
        if not content_type.startswith("image/"):
            raise ValidationException("Profile file must be an image")
        if file_size > self.MAX_PROFILE_SIZE:
            raise ValidationException("Profile image must not exceed 5 MB")

        try:
            return default_storage.save(f"profiles/{user_id}/{file_name}", uploaded_file)
        except OSError as exc:
            raise ValidationException("Unable to save profile image") from exc
