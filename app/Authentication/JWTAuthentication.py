from __future__ import annotations

# from django.utils.translation import gettext_lazy as _
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken
# from rest_framework_simplejwt.settings import api_settings

# from app.model import User


# class AppJWTAuthentication(JWTAuthentication):
#     def get_user(self, validated_token):
#         try:
#             user_id = validated_token[api_settings.USER_ID_CLAIM]
#         except KeyError:
#             raise InvalidToken(_("Token contained no recognizable user identification"))

#         try:
#             return User.objects.get(**{api_settings.USER_ID_FIELD: user_id})
#         except User.DoesNotExist:
#             raise AuthenticationFailed(_("User not found"), code="user_not_found")
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken
from rest_framework_simplejwt.settings import api_settings

from app.model import User


class AppJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        print("AUTH HEADER:", request.headers.get("Authorization"))

        try:
            result = super().authenticate(request)
            print("AUTH SUCCESS:", result)
            return result
        except Exception as e:
            print("AUTH ERROR:", type(e).__name__, str(e))
            raise

    def get_user(self, validated_token):
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
            print("TOKEN USER ID:", user_id)
        except KeyError:
            raise InvalidToken(_("Token contained no recognizable user identification"))

        try:
            user = User.objects.get(id=user_id)

            print("FOUND USER:")
            print("ID:", user.id)
            print("EMAIL:", user.email)

            return user

        except User.DoesNotExist:
            print("USER NOT FOUND:", user_id)
            print("TOTAL USERS:", User.objects.count())

            raise AuthenticationFailed(
                _("User not found"),
                code="user_not_found"
            )
