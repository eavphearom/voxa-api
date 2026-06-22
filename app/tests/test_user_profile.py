from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase
from django.urls import resolve

from app.DTO.user_dtos import UserUpdateDTO
from app.Exceptions import ValidationException
from app.Services.UserServiceImpl import UserServiceImpl


class FakeUserRepository:
    def __init__(self):
        self.user = SimpleNamespace(
            id=1,
            name="Old Name",
            email="old@example.com",
            phone="0123456789",
            role="user",
            google_id=None,
            avatar=None,
        )
        self.other_user = SimpleNamespace(id=2, email="taken@example.com", phone="0987654321")

    def find_by_id(self, user_id):
        return self.user if user_id == self.user.id else None

    def find_by_email(self, email):
        if email == self.other_user.email:
            return self.other_user
        return self.user if email == self.user.email else None

    def find_by_phone(self, phone):
        if phone == self.other_user.phone:
            return self.other_user
        return self.user if phone == self.user.phone else None

    def update(self, user, data):
        for field, value in data.items():
            setattr(user, field, value)
        return user


class UserProfileServiceTests(SimpleTestCase):
    def test_get_profile_returns_stored_avatar_path(self):
        repository = FakeUserRepository()
        repository.user.avatar = "profiles/1/avatar.png"

        result = UserServiceImpl(repository).get_profile(1)

        self.assertEqual(result["avatar"], "profiles/1/avatar.png")
        self.assertEqual(result["profile"], "profiles/1/avatar.png")

    def test_updates_name_email_and_phone(self):
        service = UserServiceImpl(FakeUserRepository())
        dto = UserUpdateDTO(
            name="New Name",
            email="NEW@EXAMPLE.COM",
            phone="+85512345678",
        )

        result = service.update_profile(1, dto)

        self.assertEqual(result["name"], "New Name")
        self.assertEqual(result["email"], "new@example.com")
        self.assertEqual(result["phone"], "+85512345678")

    def test_rejects_another_users_email(self):
        service = UserServiceImpl(FakeUserRepository())

        with self.assertRaisesMessage(ValidationException, "Email already exists"):
            service.update_profile(1, UserUpdateDTO(email="taken@example.com"))

    @patch("app.Services.UserServiceImpl.default_storage.save", return_value="profiles/1/avatar.png")
    def test_stores_uploaded_profile_image(self, save_file):
        service = UserServiceImpl(FakeUserRepository())
        image = SimpleUploadedFile("avatar.png", b"image-data", content_type="image/png")

        result = service.update_profile(1, UserUpdateDTO(profile_file=image))

        self.assertEqual(result["profile"], "profiles/1/avatar.png")
        save_file.assert_called_once()


class UserProfileRouteTests(SimpleTestCase):
    def test_profile_route_is_registered(self):
        match = resolve("/api/user/v1/profile")

        self.assertEqual(match.url_name, "user-profile")
