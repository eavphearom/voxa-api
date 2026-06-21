from django.db import models


class Meeting(models.Model):
    user_id = models.BigIntegerField()

    title = models.CharField(
        max_length=255
    )

    source_type = models.CharField(
        max_length=20
    )
    # record, audio, video

    file_name = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    file_path = models.CharField(
        max_length=1000,
        null=True,
        blank=True
    )

    file_size = models.BigIntegerField(
        default=0
    )

    duration = models.IntegerField(
        null=True,
        blank=True
    )

    language = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=50,
        default="processing"
    )
    # processing, completed, failed

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    created_uid = models.BigIntegerField(
        null=True,
        blank=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    updated_uid = models.BigIntegerField(
        null=True,
        blank=True
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    deleted_uid = models.BigIntegerField(
        null=True,
        blank=True
    )

    is_deleted = models.BooleanField(
        default=False
    )

    class Meta:
        app_label = "app"
        db_table = "meetings"

    def __str__(self):
        return self.title