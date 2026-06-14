from django.db import models
from app.Enums import Role

class User(models.Model):
    name = models.CharField(max_length=255)

    email = models.EmailField(
        unique=True
    )

    phone = models.CharField(
        max_length=30,
        unique=True
    )

    password = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    google_id = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True
    )

    avatar = models.TextField(
        null=True,
        blank=True

    )


    role = models.CharField(
        max_length=20,
        choices=[(role.value, role.value) for role in Role],
        default=Role.USER.value,
    )

    email_verified_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False
