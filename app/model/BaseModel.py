from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_uid = models.BigIntegerField(null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    updated_uid = models.BigIntegerField(null=True, blank=True)

    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_uid = models.BigIntegerField(null=True, blank=True)

    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True