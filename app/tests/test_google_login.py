from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import patch

from django.test import SimpleTestCase, override_settings
from django.urls import resolve
from google.auth.exceptions import TransportError

from app.DTO.GoogleLoginDTO import GoogleLoginDTO
from app.Exceptions import ValidationException
from app.Services.AuthServiceImpl import AuthServiceImpl


class FakeUserRepository:
    def __init__(self, user=None):
        self.user = user
        self.created_data = None

    def find_by_google_id(self, google_id):
        if self.user and self.user.google_id == google_id:
            return self.user
        return None

    def find_by_email(self, email):
        if self.user and self.user.email == email:
            return self.user
        return None

    def create(self, data):
        self.created_data = data
        self.user = SimpleNamespace(id=7, **data)
        return self.user

    def update(self, user, data):
        for field, value in data.items():
            setattr(user, field, value)
        return user


@override_settings(GOOGLE_CLIENT_ID="web-client-id.apps.googleusercontent.com")
class GoogleLoginServiceTests(SimpleTestCase):
    @patch("app.Services.AuthServiceImpl.AccessToken.for_user", return_value="jwt-token")
    @patch("app.Services.AuthServiceImpl.google_id_token.verify_oauth2_token")
    def test_creates_google_user_and_returns_existing_jwt_shape(self, verify_token, _token):
        verify_token.return_value = {
            "sub": "google-subject",
            "email": "PERSON@EXAMPLE.COM",
            "email_verified": True,
            "name": "Voxa User",
            "picture": "https://example.com/avatar.jpg",
        }
        repository = FakeUserRepository()

        result = AuthServiceImpl(repository).google_login(GoogleLoginDTO("valid-token"))

        self.assertEqual(result["access_token"], "jwt-token")
        self.assertEqual(result["user"]["email"], "person@example.com")
        self.assertEqual(repository.created_data["google_id"], "google-subject")
        self.assertIsNone(repository.created_data["phone"])
        verify_token.assert_called_once()

    def test_rejects_missing_token(self):
        with self.assertRaisesMessage(ValidationException, "Google ID token is required"):
            AuthServiceImpl(FakeUserRepository()).google_login(GoogleLoginDTO(""))

    @patch("app.Services.AuthServiceImpl.google_id_token.verify_oauth2_token")
    def test_reports_expired_token(self, verify_token):
        verify_token.side_effect = ValueError("Token expired, 1 < 2")

        with self.assertRaisesMessage(ValidationException, "Google ID token has expired"):
            AuthServiceImpl(FakeUserRepository()).google_login(GoogleLoginDTO("expired-token"))

    @patch("app.Services.AuthServiceImpl.google_id_token.verify_oauth2_token")
    def test_reports_google_transport_failure(self, verify_token):
        verify_token.side_effect = TransportError("Google certificates unavailable")

        with self.assertRaisesMessage(ValidationException, "Google token verification failed"):
            AuthServiceImpl(FakeUserRepository()).google_login(GoogleLoginDTO("token"))


class GoogleLoginRouteTests(SimpleTestCase):
    def test_google_login_route_is_registered(self):
        match = resolve("/api/user/v1/auth/google-login")

        self.assertEqual(match.url_name, "auth-google-login")
